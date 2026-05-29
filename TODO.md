# Harami Parrots — Task Breakdown

## How to Use This File

Per task workflow:
1. Write tests FIRST (red phase — confirm they fail)
2. Implement until tests pass (green phase)
3. Review diff manually — don't trust AI descriptions
4. Commit with descriptive message
5. Update `CLAUDE.md`/`AGENTS.md` with lessons learned (compound loop)

---

## Phase 0: Foundation ⬜

- [ ] Python 3.12+ environment setup (`pyproject.toml` or `requirements.txt`)
- [ ] `pytest` + `pytest-asyncio` configured, first smoke test passing
- [ ] `.env.example` with `GROK_API_KEY`, `GEMINI_API_KEY`, `NOTEBOOKLM_*` vars
- [ ] `pre-commit` hooks: `ruff` linter + `black` formatter
- [ ] GitHub Actions CI: runs `pytest tests/` on push to main
- [ ] Review and update `CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`
- [ ] Create `episodes/research/` folder conventions doc

**Evidence gate**: All tests green in CI before Phase 1.

---

## Phase 1: Research Pipeline ⬜

> Goal: Given an episode ID (e.g., `S1E01`), produce a structured research brief.

- [ ] Write tests for `researcher.py` interface (red)
- [ ] `src/pipeline/config.py` — API key loading, model selection per task
- [ ] `src/pipeline/researcher.py` — Gemini 1.5 Pro for long-context synthesis
- [ ] `src/pipeline/researcher.py` — Grok API for real-time news/social context
- [ ] NotebookLM prompt templates in `prompts/notebooklm_research.md`
- [ ] `scripts/generate_research.py` — CLI: `--episode S1E01 --output episodes/research/S1E01/brief.md`
- [ ] Implement tests green
- [ ] Manual test: run S1E01 research brief, verify output quality

**Evidence gate**: `pytest tests/test_researcher.py` all green + one manual research brief reviewed.

---

## Phase 2: Script Generation Pipeline ⬜

> Goal: Turn research brief + episode premise into a full Hinglish script.

- [ ] Write tests for `script_writer.py` (red)
- [ ] Episode script schema defined (`episodes/drafts/TEMPLATE.md`)
- [ ] `prompts/parrot_personas.md` — Mithai / Kaddu / Bijli voice guides
- [ ] `prompts/script_structure.md` — Cold open → teardown → chaos → verdict template
- [ ] `src/pipeline/script_writer.py` — Grok for Hinglish wit; Gemini for structure
- [ ] `scripts/generate_script.py` — CLI: `--episode S1E01 --draft 1`
- [ ] Implement tests green
- [ ] Manual test: generate S1E01 draft, human review and edit
- [ ] Iterate on persona prompts based on output quality
- [ ] Store prompt versions with notes in `prompts/versions/`

**Evidence gate**: `pytest tests/test_script_writer.py` green + S1E01 draft reviewed by human.

---

## Phase 3: Fact-Check & Research Depth ⬜

> Goal: Verify claims in generated scripts against sources (Johnny Harris standard).

- [ ] Write tests for `fact_checker.py` (red)
- [ ] `src/pipeline/fact_checker.py` — extract claims from script, verify via Grok/Gemini
- [ ] Citation formatter: each fact gets a source link in script footnotes
- [ ] `scripts/fact_check_script.py` — CLI: `--script episodes/drafts/S1E01.md`
- [ ] Implement tests green
- [ ] Manual review of fact-check output for S1E01

**Evidence gate**: All tests green + fact-check pass on S1E01.

---

## Phase 4: Audio / Video (TBD) ⬜

> Goal: Convert script → audio (TTS parrot voices) → optional video.

- [ ] Evaluate TTS options: ElevenLabs, Kokoro, Google TTS
- [ ] `src/audio/tts.py` — per-parrot voice mapping
- [ ] `scripts/generate_audio.py` — CLI: `--script episodes/published/S1E01.md`
- [ ] Gemini video generation research: feasibility check
- [ ] Manual test: generate audio for S1E01 cold open

**Evidence gate**: Listenable audio clip from S1E01 cold open.

---

## Phase 5: Content Ops ⬜

- [ ] `scripts/new_episode.py` — scaffolds new episode folder + research template
- [ ] Episode status tracker (simple CSV or SQLite)
- [ ] `scripts/episode_status.py` — prints status of all episodes
- [ ] Publish checklist doc in `docs/publish_checklist.md`

---

## Phase 6: Ship S1E01 ⬜

- [ ] Final human edit of S1E01 script
- [ ] Record / generate audio
- [ ] Upload to hosting (Anchor / Spotify / YouTube)
- [ ] Write show notes from script
- [ ] Post-mortem: what worked, what broke

**Evidence gate**: S1E01 live and listenable.

---

## Parking Lot 🅿️

- Listener Q&A episode format
- Live budget reaction episode (sarkari special)
- Multilingual version (pure Hindi vs Hinglish A/B test)
- Short-form clips for Instagram/YouTube Shorts from episodes
- Sponsor integration script templates (keep sarcasm, add ironic sponsor reads)
- NotebookLM podcast auto-generation as first draft → human edit workflow

---

## Lessons Learned 📝

> Update this as you build. Small observations compound into better agent output.

- _[Add lessons after Phase 0]_
