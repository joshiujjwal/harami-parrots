import asyncio
import json
import logging
from pathlib import Path

import httpx

from .config import (
    DEFAULT_CONFIG,
    MAX_RETRIES,
    RETRY_BACKOFF_BASE,
    ModelConfig,
    get_gemini_api_key,
    get_grok_api_key,
)
from .models import DataPoint, EpisodeMeta, ResearchBrief, Source

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


async def _call_gemini(prompt: str, config: ModelConfig = DEFAULT_CONFIG) -> str:
    """Call Gemini API with retry/backoff."""
    api_key = get_gemini_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.gemini_model}:generateContent"

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    async with httpx.AsyncClient(timeout=120) as client:
        for attempt in range(MAX_RETRIES):
            try:
                response = await client.post(
                    url, json=payload, params={"key": api_key}
                )
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (httpx.HTTPStatusError, httpx.TimeoutException, KeyError) as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                wait = RETRY_BACKOFF_BASE**attempt
                logger.warning(f"Gemini attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)

    raise RuntimeError("Gemini: exhausted retries")


async def _call_grok(prompt: str, config: ModelConfig = DEFAULT_CONFIG) -> str:
    """Call Grok (xAI) API with retry/backoff. Compatible with OpenAI spec."""
    api_key = get_grok_api_key()
    url = "https://api.x.ai/v1/chat/completions"

    payload = {
        "model": config.grok_model,
        "messages": [{"role": "user", "content": prompt}],
    }

    async with httpx.AsyncClient(timeout=120) as client:
        for attempt in range(MAX_RETRIES):
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Authorization": f"Bearer {api_key}"},
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except (httpx.HTTPStatusError, httpx.TimeoutException, KeyError) as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                wait = RETRY_BACKOFF_BASE**attempt
                logger.warning(f"Grok attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)

    raise RuntimeError("Grok: exhausted retries")


async def fetch_realtime_context(query: str, config: ModelConfig = DEFAULT_CONFIG) -> str:
    """Fetch real-time social/news context via Grok."""
    prompt = f"""
You are a research assistant for a satirical podcast about half-baked societal ideas.
Provide real-time context, recent news, social media discourse, and current debates around:

Topic: {query}

Focus on:
- Recent events (last 6–12 months)
- Social media reactions and discourse
- Expert opinions and public debate
- Any new developments that make this topic timely

Be factual. Cite sources where possible. Keep it concise — this is research input, not the final output.
"""
    return await _call_grok(prompt, config)


async def synthesize_sources(topic: str, sources_context: str, config: ModelConfig = DEFAULT_CONFIG) -> str:
    """Synthesize research sources using Gemini's long-context capability."""
    prompt = f"""
You are a research synthesizer for a satirical podcast. 
Synthesize the following sources into a structured research brief for this topic:

TOPIC: {topic}

SOURCES/CONTEXT:
{sources_context}

Output a structured brief with these sections:
1. CONTEXT: Why does this idea exist? Who believes it and why?
2. KEY_FACTS: 5–8 verified, citable facts (with sources)
3. DATA_POINTS: Specific statistics with sources and years
4. COUNTERARGUMENTS: The strongest arguments against the idea
5. HISTORICAL_PARALLELS: Previous times this idea was tried and what happened

Be precise. Use specific numbers. Do not make up statistics.
"""
    return await _call_gemini(prompt, config)


def _parse_research_output(raw: str, episode_id: str, models_used: list[str]) -> ResearchBrief:
    """Parse the raw LLM research output into a ResearchBrief.
    
    This is a best-effort parser — imperfect output is still useful.
    """
    sections = {
        "context": "",
        "key_facts": [],
        "data_points": [],
        "counterarguments": [],
        "sources": [],
    }

    current_section = None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        upper = line.upper()
        if "CONTEXT" in upper and line.startswith(("1.", "##", "**", "CONTEXT")):
            current_section = "context"
        elif "KEY_FACTS" in upper or "KEY FACTS" in upper:
            current_section = "key_facts"
        elif "DATA_POINTS" in upper or "DATA POINTS" in upper:
            current_section = "data_points"
        elif "COUNTERARGUMENT" in upper:
            current_section = "counterarguments"
        elif current_section == "context" and line:
            sections["context"] += line + " "
        elif current_section == "key_facts" and line.startswith(("-", "*", "•")):
            sections["key_facts"].append(line.lstrip("-*• "))
        elif current_section == "data_points" and line.startswith(("-", "*", "•")):
            sections["data_points"].append(DataPoint(value=line.lstrip("-*• "), source="LLM-generated"))
        elif current_section == "counterarguments" and line.startswith(("-", "*", "•")):
            sections["counterarguments"].append(line.lstrip("-*• "))

    return ResearchBrief(
        episode_id=episode_id,
        context=sections["context"].strip() or raw[:500],
        key_facts=sections["key_facts"] or ["(Manual review required — parser could not extract facts)"],
        data_points=sections["data_points"],
        counterarguments=sections["counterarguments"],
        sources=sections["sources"],
        models_used=models_used,
    )


async def generate_research_brief(
    episode: EpisodeMeta, config: ModelConfig = DEFAULT_CONFIG
) -> ResearchBrief:
    """Generate a full research brief for an episode.
    
    Uses Grok for real-time context and Gemini for synthesis.
    """
    logger.info(f"Generating research brief for {episode.id}: {episode.title}")

    realtime_context, synthesis = await asyncio.gather(
        fetch_realtime_context(f"{episode.premise} — {episode.angle}", config),
        synthesize_sources(
            topic=f"{episode.title}: {episode.premise}",
            sources_context=f"Angle: {episode.angle}\nPremise: {episode.premise}",
            config=config,
        ),
    )

    combined = f"REALTIME CONTEXT:\n{realtime_context}\n\nSYNTHESIS:\n{synthesis}"

    brief = _parse_research_output(
        combined,
        episode_id=episode.id,
        models_used=[config.grok_model, config.gemini_model],
    )

    logger.info(f"Research brief generated for {episode.id}: {len(brief.key_facts)} facts, {len(brief.data_points)} data points")
    return brief
