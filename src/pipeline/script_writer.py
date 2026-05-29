import logging
from pathlib import Path

from .config import DEFAULT_CONFIG, HINGLISH_WPM, ModelConfig, get_grok_api_key
from .models import EpisodeMeta, ResearchBrief, Script

import httpx
import asyncio
from .config import MAX_RETRIES, RETRY_BACKOFF_BASE

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def _load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text()


def _build_script_prompt(episode: EpisodeMeta, brief: ResearchBrief) -> str:
    personas = _load_prompt("parrot_personas.md")
    structure = _load_prompt("script_structure.md")

    facts_block = "\n".join(f"- {f}" for f in brief.key_facts)
    data_block = "\n".join(f"- {d.value} (Source: {d.source})" for d in brief.data_points)
    counter_block = "\n".join(f"- {c}" for c in brief.counterarguments)

    return f"""
You are writing a script for "Harami Parrots" — a Hinglish satirical podcast.

EPISODE: {episode.id} — {episode.title}
PREMISE (the half-baked idea being roasted): {episode.premise}
ANGLE: {episode.angle}

PERSONA GUIDE:
{personas}

SCRIPT STRUCTURE:
{structure}

RESEARCH BRIEF:
Context: {brief.context}

Key Facts:
{facts_block}

Data Points:
{data_block}

Counterarguments:
{counter_block}

INSTRUCTIONS:
1. Write a full episode script following the structure guide
2. Use HINGLISH throughout — 40% Hindi, 60% English, natural blend
3. ALL THREE parrots (Mithai, Kaddu, Bijli) must appear throughout
4. Each parrot must speak in their exact voice from the persona guide
5. Include footnote citations [^1], [^2] for key facts
6. Format: **MITHAI:**, **KADDU:**, **BIJLI:** as speaker labels
7. Stage directions in [square brackets]
8. Add estimated duration comment at the top
9. Target: 4000–5500 words

Write the complete script now:
"""


async def _call_grok_for_script(prompt: str, config: ModelConfig) -> str:
    """Call Grok API for script generation."""
    api_key = get_grok_api_key()
    url = "https://api.x.ai/v1/chat/completions"

    payload = {
        "model": config.grok_model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert Hinglish scriptwriter for satirical podcast content. You write sharp, funny, research-backed dialogue.",
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 8000,
    }

    async with httpx.AsyncClient(timeout=180) as client:
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
                logger.warning(f"Grok script attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)

    raise RuntimeError("Grok script generation: exhausted retries")


def _validate_script_has_all_parrots(content: str) -> list[str]:
    """Return list of missing parrots (should be empty for a valid script)."""
    missing = []
    for parrot in ("**MITHAI:**", "**KADDU:**", "**BIJLI:**"):
        if parrot not in content:
            missing.append(parrot)
    return missing


async def generate_script(
    episode: EpisodeMeta,
    brief: ResearchBrief,
    draft: int = 1,
    config: ModelConfig = DEFAULT_CONFIG,
) -> Script:
    """Generate a full episode script from a research brief."""
    logger.info(f"Generating script draft {draft} for {episode.id}: {episode.title}")

    prompt = _build_script_prompt(episode, brief)
    content = await _call_grok_for_script(prompt, config)

    missing_parrots = _validate_script_has_all_parrots(content)
    if missing_parrots:
        logger.warning(f"Script for {episode.id} is missing parrots: {missing_parrots}. Consider regenerating.")

    word_count = len(content.split())
    estimated_duration = round(word_count / HINGLISH_WPM, 1)

    logger.info(f"Script generated: {word_count} words, ~{estimated_duration} min")

    return Script(
        episode_id=episode.id,
        draft_number=draft,
        content=content,
        word_count=word_count,
        estimated_duration_min=estimated_duration,
    )


async def rewrite_section(
    script: Script,
    section: str,
    notes: str,
    config: ModelConfig = DEFAULT_CONFIG,
) -> Script:
    """Rewrite a specific section of a script based on notes."""
    prompt = f"""
Rewrite ONLY the following section of this podcast script.
Keep everything else the same. Maintain Hinglish tone and parrot personas.

SECTION TO REWRITE: {section}
NOTES/FEEDBACK: {notes}

CURRENT SCRIPT:
{script.content}

Return the complete updated script with only the specified section changed.
"""
    updated_content = await _call_grok_for_script(prompt, config)
    word_count = len(updated_content.split())

    return Script(
        episode_id=script.episode_id,
        draft_number=script.draft_number + 1,
        content=updated_content,
        word_count=word_count,
        estimated_duration_min=round(word_count / HINGLISH_WPM, 1),
    )
