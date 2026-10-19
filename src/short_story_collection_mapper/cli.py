"""Command-line interface."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from short_story_collection_mapper.core import (
    CollectionComparison,
    StoryMap,
    build_map,
    compare_collections,
    load_csv,
)
from short_story_collection_mapper.output import literal_text, write_reports, write_stdout


def markdown(result: StoryMap) -> str:
    """Render a readable collection map."""
    lines = [
        "# Short-story collection map",
        "",
        f"- Source rows: {result.source_rows}",
        f"- Collections: {result.collection_count}",
        f"- Unique story groups: {result.unique_story_count}",
        f"- Shared stories: {len(result.shared)}",
        f"- Exclusive stories: {len(result.exclusive)}",
        f"- Possible title collisions: {len(result.possible_collisions)}",
        "",
        "## Shared stories",
        "",
    ]
    lines.extend(
        f"- **{literal_text(story.title)}**{f' — {literal_text(story.author)}' if story.author else ''}: {', '.join(literal_text(name) for name in story.collections)}"
        for story in result.shared
    )
    lines.extend(["", "## Exclusive stories", ""])
    lines.extend(
        f"- **{literal_text(story.title)}**{f' — {literal_text(story.author)}' if story.author else ''}: {literal_text(story.collections[0])}"
        for story in result.exclusive
    )
    lines.extend(["", "## Possible collisions", ""])
    lines.extend(
        f"- `{literal_text(item.normalized_title)}`: {len(item.labels)} distinct groups"
        for item in result.possible_collisions
    )
    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    """Build the parser."""
    result = argparse.ArgumentParser(
        description="Map stories across supplied collection inventories."
    )
    result.add_argument("input", type=Path)
    result.add_argument("--compare", nargs=2, metavar=("LEFT", "RIGHT"))
    result.add_argument("--json", type=Path, dest="json_output")
    result.add_argument("--markdown", type=Path, dest="markdown_output")
    return result


def main(argv: list[str] | None = None) -> int:
    """Run the command."""
    args = parser().parse_args(argv)
    try:
        rows = load_csv(args.input)
        result: StoryMap | CollectionComparison = (
            compare_collections(rows, *args.compare) if args.compare else build_map(rows)
        )
        rendered = (
            comparison_markdown(result)
            if isinstance(result, CollectionComparison)
            else markdown(result)
        )
        reports = []
        if args.json_output:
            reports.append((args.json_output, json.dumps(result.to_dict(), indent=2) + "\n"))
        if args.markdown_output:
            reports.append((args.markdown_output, rendered))
        write_reports([args.input], reports)
        write_stdout(rendered)
    except (OSError, ValueError, csv.Error, UnicodeError) as error:
        parser().error(str(error))
    return 1 if result.possible_collisions else 0


def comparison_markdown(result: CollectionComparison) -> str:
    lines = [f"# {literal_text(result.left)} / {literal_text(result.right)}", ""]
    for label, stories in (
        ("Shared", result.shared),
        ("Only left", result.only_left),
        ("Only right", result.only_right),
    ):
        lines.extend([f"## {label}", ""])
        lines.extend(
            f"- **{literal_text(story.title)}** — {literal_text(story.author)} ({literal_text(story.identifier)})"
            for story in stories
        )
        lines.append("")
    lines.extend(["## Possible collisions", ""])
    lines.extend(
        f"- {literal_text(item.normalized_title)}: {len(item.labels)} distinct groups"
        for item in result.possible_collisions
    )
    return "\n".join(lines) + "\n"
