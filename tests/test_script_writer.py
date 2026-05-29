"""Tests for the script writer pipeline."""
import pytest
from unittest.mock import AsyncMock, patch, mock_open
from pathlib import Path

from src.pipeline.models import EpisodeMeta, ResearchBrief, Script, DataPoint
from src.pipeline.script_writer import (
    generate_script,
    rewrite_section,
    _validate_script_has_all_parrots,
    _build_script_prompt,
)


MOCK_EPISODE = EpisodeMeta(
    id="S1E01",
    season=1,
    episode=1,
    title="Startup Bharat",
    premise="Just build an app bhai",
    angle="VC culture, pivot graveyard",
)

MOCK_BRIEF = ResearchBrief(
    episode_id="S1E01",
    context="The 'just build an app' culture emerged from Startup India 2015.",
    key_facts=["India has 100+ unicorns, 80% unprofitable", "Only 10% survive 5 years"],
    data_points=[DataPoint(value="72% founders never ran a business", source="Inc42 2022")],
    counterarguments=["Some apps genuinely solved problems"],
    sources=[],
    models_used=["grok-beta", "gemini-1.5-pro"],
)

VALID_SCRIPT_CONTENT = """
> Estimated duration: ~28 min

## Cold Open

**MITHAI:** Bhai, app banao, sab theek ho jayega!

**KADDU:** Is that so. Please continue.

**BIJLI:** Actually, according to Inc42's 2022 report, 72% of founders have never run a business before.

## The Idea Setup

**MITHAI:** No, listen yaar. This time it's different.

**KADDU:** Maine pehle bola tha.

**BIJLI:** The data suggests otherwise.
"""

SCRIPT_MISSING_BIJLI = """
**MITHAI:** Bhai, yeh idea acha hai.
**KADDU:** Maine pehle bola tha.
"""


class TestValidateScriptHasAllParrots:
    def test_should_return_empty_list_when_all_parrots_present(self):
        missing = _validate_script_has_all_parrots(VALID_SCRIPT_CONTENT)
        assert missing == []

    def test_should_return_missing_parrot_name_when_absent(self):
        missing = _validate_script_has_all_parrots(SCRIPT_MISSING_BIJLI)
        assert "**BIJLI:**" in missing

    def test_should_detect_all_missing_parrots_when_script_is_empty(self):
        missing = _validate_script_has_all_parrots("")
        assert len(missing) == 3

    def test_should_return_empty_list_for_full_valid_script(self):
        assert _validate_script_has_all_parrots(VALID_SCRIPT_CONTENT) == []


class TestGenerateScript:
    @pytest.mark.asyncio
    async def test_should_return_script_object_when_generation_succeeds(self):
        mock_personas = "# Parrot Personas\nMithai: optimistic\nKaddu: cynical\nBijli: data"
        mock_structure = "# Script Structure\nCold Open → Setup → Teardown → Verdict"

        with (
            patch("src.pipeline.script_writer._call_grok_for_script", new_callable=AsyncMock) as mock_grok,
            patch("builtins.open", mock_open(read_data=mock_personas)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.read_text", side_effect=[mock_personas, mock_structure]),
        ):
            mock_grok.return_value = VALID_SCRIPT_CONTENT
            script = await generate_script(MOCK_EPISODE, MOCK_BRIEF)

            assert isinstance(script, Script)
            assert script.episode_id == "S1E01"
            assert script.draft_number == 1

    @pytest.mark.asyncio
    async def test_should_calculate_word_count_from_content(self):
        with (
            patch("src.pipeline.script_writer._call_grok_for_script", new_callable=AsyncMock) as mock_grok,
            patch("pathlib.Path.read_text", side_effect=["personas", "structure"]),
            patch("pathlib.Path.exists", return_value=True),
        ):
            mock_grok.return_value = VALID_SCRIPT_CONTENT
            script = await generate_script(MOCK_EPISODE, MOCK_BRIEF)
            assert script.word_count == len(VALID_SCRIPT_CONTENT.split())

    @pytest.mark.asyncio
    async def test_should_estimate_duration_from_word_count(self):
        with (
            patch("src.pipeline.script_writer._call_grok_for_script", new_callable=AsyncMock) as mock_grok,
            patch("pathlib.Path.read_text", side_effect=["personas", "structure"]),
            patch("pathlib.Path.exists", return_value=True),
        ):
            mock_grok.return_value = VALID_SCRIPT_CONTENT
            script = await generate_script(MOCK_EPISODE, MOCK_BRIEF)
            expected = round(script.word_count / 140, 1)
            assert script.estimated_duration_min == expected

    @pytest.mark.asyncio
    async def test_should_set_draft_number_from_parameter(self):
        with (
            patch("src.pipeline.script_writer._call_grok_for_script", new_callable=AsyncMock) as mock_grok,
            patch("pathlib.Path.read_text", side_effect=["personas", "structure"]),
            patch("pathlib.Path.exists", return_value=True),
        ):
            mock_grok.return_value = VALID_SCRIPT_CONTENT
            script = await generate_script(MOCK_EPISODE, MOCK_BRIEF, draft=3)
            assert script.draft_number == 3

    @pytest.mark.asyncio
    async def test_should_raise_when_prompt_templates_missing(self):
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError):
                await generate_script(MOCK_EPISODE, MOCK_BRIEF)


class TestRewriteSection:
    @pytest.mark.asyncio
    async def test_should_return_script_with_incremented_draft_number(self):
        existing_script = Script(
            episode_id="S1E01",
            draft_number=1,
            content=VALID_SCRIPT_CONTENT,
            word_count=100,
            estimated_duration_min=5.0,
        )

        with (
            patch("src.pipeline.script_writer._call_grok_for_script", new_callable=AsyncMock) as mock_grok,
        ):
            mock_grok.return_value = VALID_SCRIPT_CONTENT + "\n[Updated cold open]"
            updated = await rewrite_section(existing_script, "Cold Open", "Make it punchier")

            assert updated.draft_number == 2
            assert updated.episode_id == "S1E01"

    @pytest.mark.asyncio
    async def test_should_include_feedback_in_rewrite_prompt(self):
        existing_script = Script(
            episode_id="S1E01",
            draft_number=1,
            content=VALID_SCRIPT_CONTENT,
            word_count=100,
            estimated_duration_min=5.0,
        )

        with patch("src.pipeline.script_writer._call_grok_for_script", new_callable=AsyncMock) as mock_grok:
            mock_grok.return_value = VALID_SCRIPT_CONTENT
            await rewrite_section(existing_script, "Verdict", "add more Bijli data")
            prompt_used = mock_grok.call_args[0][0]
            assert "add more Bijli data" in prompt_used
