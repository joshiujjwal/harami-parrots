# Harami Parrots 🦜🦜🦜

> *Teen harami toton ka society pe sarcastic nazar. Ek episode, ek half-baked idea, aur parrots ka full opinion.*

![Status](https://img.shields.io/badge/status-🚧%20Early%20Development-yellow)
![Language](https://img.shields.io/badge/language-Hinglish-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## What Is This?

**Harami Parrots** is a research-driven satirical podcast where three opinionated parrots tear apart one half-baked idea per episode — startup delusions, government schemes, social media myths, and the general nonsense modern society has agreed to take seriously.

Research depth à la **Johnny Harris** and **Search Party**. Financial lens from **2 and 20**. Data storytelling from **Think School**. Delivered by three birds who genuinely do not care.

---

## The Cast

| Parrot | Vibe |
|--------|------|
| 🟡 **Mithai** | Delusionally optimistic. Believes every scheme. Always wrong. |
| 🟢 **Kaddu** | Ex-consultant cynic. Seen it all. Will remind you. |
| 🔴 **Bijli** | Research parrot. Drops IMF reports mid-argument. |

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Research | NotebookLM + Grok + Gemini 1.5 Pro |
| Script Generation | Python + Grok API + Gemini API |
| Voice/Audio | TBD (ElevenLabs / Kokoro TTS) |
| Video | Gemini video generation / manual edit |
| Scripts | Markdown in `episodes/` |
| Pipeline | Python 3.12+ |

---

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/harami-parrots
cd harami-parrots

# Install dependencies
pip install -r requirements.txt

# Copy env template
cp .env.example .env
# Add your API keys: GROK_API_KEY, GEMINI_API_KEY

# Run tests first (always)
pytest tests/ -v

# Generate research brief for an episode
python scripts/generate_research.py --episode S1E01

# Generate script draft
python scripts/generate_script.py --episode S1E01
```

---

## Project Structure

```
harami-parrots/
├── src/
│   ├── pipeline/
│   │   ├── researcher.py       # Multi-source research aggregation
│   │   ├── script_writer.py    # Script generation via Grok/Gemini
│   │   ├── fact_checker.py     # Claim verification pipeline
│   │   └── config.py           # API config, model selection
│   ├── audio/
│   │   └── tts.py              # TTS integration
│   └── utils/
│       └── prompts.py          # Prompt templates
├── tests/                      # Test suite (mirrors src/)
├── episodes/
│   ├── drafts/                 # WIP scripts (Markdown)
│   ├── published/              # Final scripts
│   ├── research/               # Per-episode research sources
│   └── transcripts/            # Post-recording transcripts
├── prompts/                    # Reusable AI prompt templates
├── scripts/                    # CLI automation scripts
├── docs/
│   ├── spec.md                 # Full feature spec
│   └── adr/                    # Architecture decisions
├── .github/
│   └── copilot-instructions.md
├── episode_list.md             # Master episode index (ALL seasons)
├── README.md
├── TODO.md
├── CLAUDE.md
└── AGENTS.md
```

---

## Episode Format

Each episode (`~25–35 min`) follows:

1. **Cold Open** — Sarcastic hook, establish the half-baked idea
2. **Problem Setup** — Why does this idea exist? Who believes it?
3. **Research Teardown** — Data, history, precedents (Bijli goes off)
4. **Parrot Chaos** — Mithai defends, Kaddu destroys, Bijli fact-checks
5. **Verdict** — Final sarcastic conclusion
6. **Listener Homework** — One actual thing to read/watch

---

## Contributing

- Write tests first. Always. (`red → green`)
- Keep PRs small and focused on one thing
- Include evidence: screenshots of test runs, research citations
- Review AI-generated descriptions before committing them — they lie
- Update `CLAUDE.md` or `AGENTS.md` if you learn something new

---

## Episode Index

See [`episode_list.md`](./episode_list.md) — 30+ episodes across 3 seasons + specials.
