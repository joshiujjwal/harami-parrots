# GitHub Copilot Instructions — Harami Parrots

## Project Context

Satirical podcast pipeline. Three parrot personas roast one half-baked societal idea per episode.
Research-driven (Johnny Harris depth). Hinglish language. Python 3.12+ backend.

## Stack

- Python 3.12+, `asyncio`, `httpx` for API calls
- Grok API (xAI) — Hinglish dialogue, real-time context
- Gemini 1.5 Pro API — long-context research synthesis
- `pytest` + `pytest-asyncio` for testing
- `ruff` + `black` for linting/formatting

## Coding Conventions

- All API calls are `async` — use `httpx.AsyncClient`, never `requests`
- Type hint everything: `def write_script(episode_id: str, brief: ResearchBrief) -> Script`
- Error handling: catch specific exceptions, never bare `except:`
- Prompt templates load from `prompts/` directory — never hardcode prompts in `src/`
- Config from `.env` via `python-dotenv` — fail fast if keys missing at startup
- Return typed dataclasses or Pydantic models from pipeline functions, not raw dicts

## Testing Conventions

- Mock all external APIs using `pytest-mock` or `unittest.mock`
- Test files mirror source structure
- Pattern: `test_should_<behavior>_when_<condition>`
- Always write the failing test first before implementing anything

## Parrot Persona Rules (Critical)

When generating any dialogue or script content:
- **Mithai** starts enthusiastic, uses "bhai/yaar", defends the idea, gets proven wrong
- **Kaddu** is measured and dry, references past predictions, never raises voice
- **Bijli** interrupts with citations, says "Actually, according to [source]..."
- All three must appear in every episode script — never skip a parrot

## Boundaries

- Only modify files explicitly discussed
- Do not refactor code that isn't part of the current task
- Do not remove existing tests — ever
- Do not change parrot personas without updating `prompts/parrot_personas.md` first
- Do not add new dependencies without updating `requirements.txt`
- Ask before making changes across more than 3 files at once
