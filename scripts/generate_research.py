"""CLI: Generate research brief for an episode."""
import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import generate_research_brief
from src.pipeline.models import EpisodeMeta

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

EPISODES: dict[str, EpisodeMeta] = {
    "S1E01": EpisodeMeta(
        id="S1E01", season=1, episode=1,
        title="Startup Bharat: How Everyone Became a Founder Without Founding Anything",
        premise="Just build an app bhai — it solves everything",
        angle="VC ecosystem, idea culture, the pivot graveyard",
    ),
    "S1E02": EpisodeMeta(
        id="S1E02", season=1, episode=2,
        title="Superpower by 2030™ — The Subscription Plan",
        premise="India will be superpower in exactly 7 years",
        angle="GDP dreams vs HDI reality, the deadline that keeps moving",
    ),
    "S1E03": EpisodeMeta(
        id="S1E03", season=1, episode=3,
        title="Crypto Saved My Cousin's Life (He Lost ₹4 Lakh)",
        premise="Crypto is freedom from banks",
        angle="DeFi promises, regulatory whiplash, the WhatsApp uncle pipeline",
    ),
    # Add more from episode_list.md as needed
}


async def main(episode_id: str, output_dir: Path) -> None:
    if episode_id not in EPISODES:
        print(f"Error: Episode {episode_id} not found. Known episodes: {list(EPISODES.keys())}")
        sys.exit(1)

    episode = EPISODES[episode_id]
    print(f"Generating research brief for {episode_id}: {episode.title}")

    brief = await generate_research_brief(episode)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "brief.md"

    with open(output_path, "w") as f:
        f.write(f"# Research Brief: {episode.title}\n\n")
        f.write(f"**Episode**: {episode.id}  \n")
        f.write(f"**Premise**: {episode.premise}  \n")
        f.write(f"**Angle**: {episode.angle}  \n\n")
        f.write("---\n\n")
        f.write(f"## Context\n\n{brief.context}\n\n")
        f.write("## Key Facts\n\n")
        for fact in brief.key_facts:
            f.write(f"- {fact}\n")
        f.write("\n## Data Points\n\n")
        for dp in brief.data_points:
            f.write(f"- {dp.value} *(Source: {dp.source})*\n")
        f.write("\n## Counterarguments\n\n")
        for ca in brief.counterarguments:
            f.write(f"- {ca}\n")
        f.write(f"\n---\n*Generated using: {', '.join(brief.models_used)}*\n")

    print(f"Research brief saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate research brief for an episode")
    parser.add_argument("--episode", required=True, help="Episode ID (e.g., S1E01)")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: episodes/research/<episode_id>/)",
    )
    args = parser.parse_args()

    output_dir = args.output or Path(f"episodes/research/{args.episode}")
    asyncio.run(main(args.episode, output_dir))
