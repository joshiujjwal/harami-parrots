"""Tests for the research pipeline."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.pipeline.models import EpisodeMeta, ResearchBrief, DataPoint
from src.pipeline.researcher import (
    fetch_realtime_context,
    synthesize_sources,
    generate_research_brief,
    _parse_research_output,
)


MOCK_EPISODE = EpisodeMeta(
    id="S1E01",
    season=1,
    episode=1,
    title="Startup Bharat: How Everyone Became a Founder Without Founding Anything",
    premise="Just build an app bhai — it solves everything",
    angle="VC ecosystem, idea culture, the pivot graveyard",
)

MOCK_GROK_RESPONSE = """
Recent news: The Indian startup ecosystem saw 70 unicorns by 2023, but 40+ 
have cut valuations significantly. Ed-tech sector saw mass layoffs in 2022-23.
Key debate on LinkedIn: 'Is hustle culture toxic?' getting 100k+ engagements.
"""

MOCK_GEMINI_RESPONSE = """
CONTEXT: The 'just build an app' culture emerged from the 2015 Startup India initiative.
KEY_FACTS:
- India has 100+ unicorns but 80% are still unprofitable (2023)
- Only 10% of Indian startups survive beyond 5 years
- Bangalore alone has 15,000+ registered startups
DATA_POINTS:
- 72% of Indian startup founders have never run a business before (Inc42, 2022)
COUNTERARGUMENTS:
- Some apps genuinely solved real problems (Zepto, CRED)
- Access to capital has democratized entrepreneurship
"""


class TestFetchRealtimeContext:
    @pytest.mark.asyncio
    async def test_should_return_string_when_grok_succeeds(self):
        with patch("src.pipeline.researcher._call_grok", new_callable=AsyncMock) as mock_grok:
            mock_grok.return_value = MOCK_GROK_RESPONSE
            result = await fetch_realtime_context("Indian startup culture")
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_should_pass_query_in_prompt_to_grok(self):
        with patch("src.pipeline.researcher._call_grok", new_callable=AsyncMock) as mock_grok:
            mock_grok.return_value = MOCK_GROK_RESPONSE
            await fetch_realtime_context("crypto bhai")
            call_args = mock_grok.call_args[0][0]
            assert "crypto bhai" in call_args

    @pytest.mark.asyncio
    async def test_should_raise_when_grok_fails(self):
        with patch("src.pipeline.researcher._call_grok", new_callable=AsyncMock) as mock_grok:
            mock_grok.side_effect = RuntimeError("API error")
            with pytest.raises(RuntimeError):
                await fetch_realtime_context("any query")


class TestSynthesizeSources:
    @pytest.mark.asyncio
    async def test_should_return_synthesis_string_when_gemini_succeeds(self):
        with patch("src.pipeline.researcher._call_gemini", new_callable=AsyncMock) as mock_gemini:
            mock_gemini.return_value = MOCK_GEMINI_RESPONSE
            result = await synthesize_sources("startup culture", "some sources here")
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_should_include_topic_in_gemini_prompt(self):
        with patch("src.pipeline.researcher._call_gemini", new_callable=AsyncMock) as mock_gemini:
            mock_gemini.return_value = MOCK_GEMINI_RESPONSE
            await synthesize_sources("jugaad innovation", "context here")
            call_args = mock_gemini.call_args[0][0]
            assert "jugaad innovation" in call_args


class TestParseResearchOutput:
    def test_should_return_research_brief_with_episode_id(self):
        brief = _parse_research_output(MOCK_GEMINI_RESPONSE, "S1E01", ["gemini-1.5-pro"])
        assert brief.episode_id == "S1E01"

    def test_should_extract_key_facts_from_structured_output(self):
        brief = _parse_research_output(MOCK_GEMINI_RESPONSE, "S1E01", ["gemini-1.5-pro"])
        assert len(brief.key_facts) > 0

    def test_should_extract_counterarguments_when_present(self):
        brief = _parse_research_output(MOCK_GEMINI_RESPONSE, "S1E01", ["gemini-1.5-pro"])
        assert len(brief.counterarguments) > 0

    def test_should_record_models_used(self):
        models = ["grok-beta", "gemini-1.5-pro"]
        brief = _parse_research_output(MOCK_GEMINI_RESPONSE, "S1E01", models)
        assert brief.models_used == models

    def test_should_handle_empty_input_gracefully(self):
        brief = _parse_research_output("", "S1E99", [])
        assert brief.episode_id == "S1E99"
        assert isinstance(brief.key_facts, list)


class TestGenerateResearchBrief:
    @pytest.mark.asyncio
    async def test_should_return_research_brief_for_valid_episode(self):
        with (
            patch("src.pipeline.researcher._call_grok", new_callable=AsyncMock) as mock_grok,
            patch("src.pipeline.researcher._call_gemini", new_callable=AsyncMock) as mock_gemini,
        ):
            mock_grok.return_value = MOCK_GROK_RESPONSE
            mock_gemini.return_value = MOCK_GEMINI_RESPONSE

            brief = await generate_research_brief(MOCK_EPISODE)

            assert isinstance(brief, ResearchBrief)
            assert brief.episode_id == "S1E01"
            assert len(brief.models_used) == 2

    @pytest.mark.asyncio
    async def test_should_call_both_grok_and_gemini(self):
        with (
            patch("src.pipeline.researcher._call_grok", new_callable=AsyncMock) as mock_grok,
            patch("src.pipeline.researcher._call_gemini", new_callable=AsyncMock) as mock_gemini,
        ):
            mock_grok.return_value = MOCK_GROK_RESPONSE
            mock_gemini.return_value = MOCK_GEMINI_RESPONSE

            await generate_research_brief(MOCK_EPISODE)

            assert mock_grok.called
            assert mock_gemini.called

    @pytest.mark.asyncio
    async def test_should_fail_fast_if_both_providers_fail(self):
        with (
            patch("src.pipeline.researcher._call_grok", new_callable=AsyncMock) as mock_grok,
            patch("src.pipeline.researcher._call_gemini", new_callable=AsyncMock) as mock_gemini,
        ):
            mock_grok.side_effect = RuntimeError("Grok down")
            mock_gemini.side_effect = RuntimeError("Gemini down")

            with pytest.raises(RuntimeError):
                await generate_research_brief(MOCK_EPISODE)
