import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    grok_model: str = "grok-beta"
    gemini_model: str = "gemini-1.5-pro"
    research_provider: str = "gemini"  # gemini | grok
    script_provider: str = "grok"  # grok excels at Hinglish
    fact_check_provider: str = "gemini"


def get_grok_api_key() -> str:
    key = os.getenv("GROK_API_KEY")
    if not key:
        raise EnvironmentError("GROK_API_KEY not set. Add it to your .env file.")
    return key


def get_gemini_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise EnvironmentError("GEMINI_API_KEY not set. Add it to your .env file.")
    return key


# Words per minute for Hinglish podcast speech (slower than pure English)
HINGLISH_WPM = 140

# Target episode duration range
MIN_EPISODE_WORDS = 3500
MAX_EPISODE_WORDS = 5500

# Retry config for API calls
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2.0  # seconds, exponential

DEFAULT_CONFIG = ModelConfig()
