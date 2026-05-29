# CLAUDE.md — Harami Parrots

## What This Is

Research-driven satirical podcast. Three parrot personas (Mithai/Kaddu/Bijli) roast one half-baked societal idea per episode. Python pipeline automates research + script generation via Grok, Gemini, and NotebookLM.

---

## Commands

```bash
# Always run tests first when starting a session
pytest tests/ -v

# Lint + format
ruff check src/ tests/
black src/ tests/

# Research brief for an episode
python scripts/generate_research.py --episode S1E01

# Script generation
python scripts/generate_script.py --episode S1E01 --draft 1

# Fact check a draft
python scripts/fact_check_script.py --script episodes/drafts/S1E01.md

# New episode scaffold
python scripts/new_episode.py --id S1E02 --title "Your Title" --idea "The half-baked idea"
```

---

## Directory Map

```
src/pipeline/     → Core AI pipeline: researcher, script_writer, fact_checker
src/audio/        → TTS generation, voice-per-parrot mapping
src/utils/        → Shared utilities, prompt loading
tests/            → Mirror of src/ — test_researcher.py, test_script_writer.py, etc.
episodes/
  drafts/         → WIP scripts, Markdown, one file per episode (S1E01.md)
  published/      → Human-approved final scripts
  research/       → Per-episode: sources.md, grok_queries.md, gemini_prompts.md
  transcripts/    → Post-recording transcripts
prompts/          → Reusable prompt templates, versioned
scripts/          → CLI entry points (not src — these are thin wrappers)
docs/spec.md      → Feature spec (read this before implementing anything new)
episode_list.md   → Master list of ALL episodes — 3 seasons + specials
```

---

## AI Model Assignments

| Task | Model | Why |
|------|-------|-----|
| Long-context research synthesis | Gemini 1.5 Pro | 1M context window |
| Real-time news / social pulse | Grok | X/Twitter integration |
| Hinglish wit, dialogue writing | Grok | Strong colloquial Hinglish |
| Structured script generation | Gemini | Better at following format |
| Fact-check verification | Gemini + Grok | Cross-reference |
| NotebookLM | Manual / API | Deep PDF/report synthesis |

---

## Parrot Voices — NON-NEGOTIABLE

These personas must be consistent across ALL generated content:

- **Mithai** 🟡: Enthusiastic, uses "bhai" constantly, starts with "Yaar, I was thinking..." — always defends the half-baked idea initially, gets destroyed by data
- **Kaddu** 🟢: Dry, measured, ex-consultant energy, uses "Maine pehle bola tha" — has receipts, never yells, most devastating when calm
- **Bijli** 🔴: Fact-drops mid-conversation, cites obscure papers, interrupts with "Actually, according to..." — not mean, just relentlessly accurate

---

## Script Format Conventions

- Language: Hinglish (Hindi words with English grammar flow, or vice versa)
- Tone: Sarcastic but informed — not mean-spirited, not preachy
- Each episode must have a **real factual claim** as its foundation — no made-up stats
- Cold open must hook in < 60 seconds of dialogue
- Verdict must be one punchy line per parrot

---

## Workflow

1. **Run tests first**: `pytest tests/ -v` — understand current state
2. **Check TODO.md**: Find the current phase, pick the next unchecked task
3. **Red phase**: Write failing tests for what you're building
4. **Green phase**: Implement until tests pass
5. **Review diff**: Read every changed line — AI writes convincingly wrong code
6. **Commit**: Descriptive message, small scope
7. **Update this file**: If you hit a gotcha or convention, add it here

---

## Gotchas

- Gemini API rate limits are aggressive on free tier — build in retry/backoff
- Grok API response format differs from OpenAI spec — check `config.py` for adapter
- NotebookLM has no public API (as of 2024) — use `prompts/notebooklm_research.md` as manual guide
- Episode IDs are `S{season}E{episode}` zero-padded: `S1E01`, `S1E10`, `S2E01`
- Hinglish generation quality varies — always human-review before publishing
