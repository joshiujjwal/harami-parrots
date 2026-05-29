"""CLI: Generate script draft for an episode."""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import generate_research_brief, generate_script
from scripts.generate_research import EPISODES

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


async def main(episode_id: str, draft: int, output_dir: Path) -> None:
    if episode_id not in EPISODES:
        print(f"Error: Episode {episode_id} not found.")
        sys.exit(1)

    episode = EPISODES[episode_id]
    print(f"Step 1/2: Generating research brief for {episode_id}...")

    brief = await generate_research_brief(episode)

    print(f"Step 2/2: Generating script draft {draft}...")
    script = await generate_script(episode, brief, draft=draft)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{episode_id}_draft{draft}.md"

    output_path.write_text(script.content)

    print(f"\n✓ Script saved: {output_path}")
    print(f"  Word count: {script.word_count}")
    print(f"  Estimated duration: ~{script.estimated_duration_min} min")
    print(f"  Fact-check status: {script.fact_check_status}")
    print("\nNext step: Human review required before publishing.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate script for an episode")
    parser.add_argument("--episode", required=True, help="Episode ID (e.g., S1E01)")
    parser.add_argument("--draft", type=int, default=1, help="Draft number (default: 1)")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("episodes/drafts"),
        help="Output directory (default: episodes/drafts/)",
    )
    args = parser.parse_args()
    asyncio.run(main(args.episode, args.draft, args.output))
