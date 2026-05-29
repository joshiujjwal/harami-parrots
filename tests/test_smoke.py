"""Smoke test — verifies the project is set up correctly."""
import importlib
import pytest


def test_should_import_pipeline_package():
    pipeline = importlib.import_module("src.pipeline")
    assert pipeline is not None


def test_should_import_all_models():
    from src.pipeline.models import (
        EpisodeMeta,
        ResearchBrief,
        Script,
        DataPoint,
        Source,
        ClaimVerification,
        AnnotatedScript,
    )
    assert EpisodeMeta is not None
    assert ResearchBrief is not None
    assert Script is not None


def test_should_create_episode_meta():
    from src.pipeline.models import EpisodeMeta
    ep = EpisodeMeta(
        id="S1E01",
        season=1,
        episode=1,
        title="Test Episode",
        premise="The half-baked idea",
        angle="The angle",
    )
    assert ep.id == "S1E01"
    assert ep.season == 1


def test_should_import_config_without_crashing():
    """Config import should not fail even without env vars set."""
    from src.pipeline import config
    assert config.HINGLISH_WPM == 140
    assert config.MAX_RETRIES == 3


def test_should_raise_on_missing_grok_key(monkeypatch):
    monkeypatch.delenv("GROK_API_KEY", raising=False)
    from src.pipeline.config import get_grok_api_key
    with pytest.raises(EnvironmentError, match="GROK_API_KEY"):
        get_grok_api_key()


def test_should_raise_on_missing_gemini_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    from src.pipeline.config import get_gemini_api_key
    with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
        get_gemini_api_key()
