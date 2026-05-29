# AGENTS.md — Harami Parrots

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Add GROK_API_KEY, GEMINI_API_KEY
pytest tests/ -v       # Run tests first — always
```

## Code Style (Python 3.12+)

- `ruff` for linting, `black` for formatting — both run in pre-commit
- Type hints on all function signatures
- `async/await` for all API calls — never sync HTTP in pipeline code
- Early returns to reduce nesting — no deeply nested if/else
- Named exports only — no `from module import *`
- Descriptive variable names — `episode_id` not `eid`, `research_brief` not `brief`
- Constants in `SCREAMING_SNAKE_CASE` in `config.py`

## Testing (Red/Green TDD)

```bash
pytest tests/ -v                          # All tests
pytest tests/test_researcher.py -v        # Specific module
pytest tests/ -k "test_script" -v         # Pattern match
pytest tests/ --tb=short                  # Shorter tracebacks
```

- **Write tests FIRST. Confirm they fail (red). Then implement (green).**
- Test file names mirror source: `src/pipeline/researcher.py` → `tests/test_researcher.py`
- Test names: `test_should_<behavior>_when_<condition>`
- Mock all external API calls in tests — no real API calls in test suite
- Include edge cases: empty input, API timeout, malformed response
- Never delete existing tests

## Project-Specific Rules

- Episode IDs format: `S1E01`, `S2E10` (season + episode, zero-padded)
- Scripts live in `episodes/drafts/` as `S1E01.md` — never in `src/`
- All prompts are templates in `prompts/` — script_writer loads them, never hardcodes
- Parrot personas (Mithai/Kaddu/Bijli) must match `prompts/parrot_personas.md` exactly
- Research briefs go in `episodes/research/<episode_id>/brief.md`

## PR Instructions

- Keep PRs to one logical change
- Include evidence: paste test output, show example script excerpt, note API response quality
- Review AI-generated commit descriptions — they overstate things
- Tag PRs: `pipeline`, `content`, `infra`, `prompts`

## Key Files to Read Before Coding

- `docs/spec.md` — full feature spec
- `episode_list.md` — all episodes, premise, angle
- `prompts/parrot_personas.md` — persona voice guide (do not drift from this)
- `CLAUDE.md` — AI model assignments, gotchas
