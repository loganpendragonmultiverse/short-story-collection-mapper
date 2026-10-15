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
        f"- **{story.title}**{f' — {story.author}' if story.author else ''}: {', '.join(story.collections)}"
        for story in result.shared
    )
    lines.extend(["", "## Exclusive stories", ""])
    lines.extend(
        f"- **{story.title}**{f' — {story.author}' if story.author else ''}: {story.collections[0]}"
        for story in result.exclusive
    )
    lines.extend(["", "## Possible collisions", ""])
    lines.extend(
        f"- `{item.normalized_title}`: {len(item.labels)} distinct groups"
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
    except (OSError, ValueError, csv.Error) as error:
        parser().error(str(error))
    rendered = (
        comparison_markdown(result)
        if isinstance(result, CollectionComparison)
        else markdown(result)
    )
    if args.json_output:
        args.json_output.write_text(json.dumps(result.to_dict(), indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if result.possible_collisions else 0


def comparison_markdown(result: CollectionComparison) -> str:
    lines = [f"# {result.left} / {result.right}", ""]
    for label, stories in (
        ("Shared", result.shared),
        ("Only left", result.only_left),
        ("Only right", result.only_right),
    ):
        lines.extend([f"## {label}", ""])
        lines.extend(
            f"- **{story.title}** — {story.author} ({story.identifier})" for story in stories
        )
        lines.append("")
    lines.extend(["## Possible collisions", ""])
    lines.extend(
        f"- {item.normalized_title}: {len(item.labels)} distinct groups"
        for item in result.possible_collisions
    )
    return "\n".join(lines) + "\n"
