"""CLI: Scaffold a new episode folder with research templates."""
import argparse
import sys
from pathlib import Path
from datetime import datetime

RESEARCH_TEMPLATE = """# Research: {title}

**Episode**: {id}  
**Premise**: {idea}  
**Date created**: {date}

---

## NotebookLM Upload Set

Upload these to NotebookLM and use `prompts/notebooklm_research.md` as your query guide:

- [ ] Wikipedia article on the topic
- [ ] Relevant government reports / policy documents
- [ ] 2–3 news articles (recent, < 1 year)
- [ ] 1 academic paper or think tank report
- [ ] 1 critical/contrarian piece

## Grok Queries

Run these in `scripts/generate_research.py --episode {id}` or manually:

```
- Current discourse: "What are people saying about [topic] in 2024?"
- Recent news: "[topic] news last 6 months India"
- Social media: "Twitter debate [topic] India"
```

## Gemini Synthesis Prompts

```
- "Synthesize the history and failures of [idea] across 5 countries"
- "What does economic research say about [idea]? Provide citations."
- "Who benefits from [idea] and who bears the costs?"
```

## Key Questions to Answer

- [ ] Why does this idea exist? What's the origin?
- [ ] Who promotes it and what are their incentives?
- [ ] Has this been tried before? Results?
- [ ] What does the data actually say?
- [ ] What's the strongest argument FOR the idea?

## Notes

_Research notes go here_
"""

SOURCES_TEMPLATE = """# Sources: {title}

| # | Title | URL | Type | Credibility |
|---|-------|-----|------|-------------|
| 1 | | | article | |
| 2 | | | report | |
| 3 | | | paper | |

## Data Points Found

| Stat | Value | Source | Year |
|------|-------|--------|------|
| | | | |
"""


def scaffold_episode(episode_id: str, title: str, idea: str, base_dir: Path) -> None:
    research_dir = base_dir / "episodes" / "research" / episode_id
    research_dir.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")

    (research_dir / "notes.md").write_text(
        RESEARCH_TEMPLATE.format(id=episode_id, title=title, idea=idea, date=date)
    )
    (research_dir / "sources.md").write_text(
        SOURCES_TEMPLATE.format(title=title)
    )

    drafts_dir = base_dir / "episodes" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    draft_path = drafts_dir / f"{episode_id}_draft0.md"
    draft_path.write_text(f"""# {title}

**Episode**: {episode_id}  
**Premise**: {idea}  
**Status**: 🟡 Research phase

---

_Script draft goes here. Run `scripts/generate_script.py --episode {episode_id}` to auto-generate._
""")

    print(f"✓ Created episode scaffold for {episode_id}")
    print(f"  Research dir: {research_dir}")
    print(f"  Draft placeholder: {draft_path}")
    print(f"\nNext steps:")
    print(f"  1. Add sources to {research_dir}/sources.md")
    print(f"  2. Run: python scripts/generate_research.py --episode {episode_id}")
    print(f"  3. Run: python scripts/generate_script.py --episode {episode_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new episode")
    parser.add_argument("--id", required=True, help="Episode ID (e.g., S2E01)")
    parser.add_argument("--title", required=True, help="Episode title")
    parser.add_argument("--idea", required=True, help="The half-baked idea being roasted")
    args = parser.parse_args()

    scaffold_episode(args.id, args.title, args.idea, Path("."))
