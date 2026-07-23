"""Behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from short_story_collection_mapper.cli import main, markdown
from short_story_collection_mapper.core import StoryRow, build_map, load_csv, normalize, story_key


def write(path: Path, text: str) -> Path:
    """Write a CSV fixture."""
    path.write_text(text, encoding="utf-8")
    return path


def test_normalization() -> None:
    assert normalize("  The—Story! ") == "the story"


def test_identifier_takes_priority() -> None:
    assert story_key(StoryRow("A", "Title", "Author", "ISFDB-1")) == "id:isfdb 1"


def test_map_shared_exclusive_and_collision() -> None:
    result = build_map(
        [
            StoryRow("One", "The Door", "A. Writer"),
            StoryRow("Two", "The Door", "A. Writer"),
            StoryRow("One", "Only Here", "A. Writer"),
            StoryRow("Three", "The Door", "B. Writer"),
        ]
    )
    assert result.collection_count == 3
    assert result.shared[0].collections == ("One", "Two")
    assert len(result.exclusive) == 2
    assert result.possible_collisions[0].normalized_title == "the door"


def test_csv_case_insensitive_headers(tmp_path: Path) -> None:
    path = write(tmp_path / "stories.csv", "Collection,Title,Author\nBook,Story,Writer\n")
    assert load_csv(path) == [StoryRow("Book", "Story", "Writer", "")]


@pytest.mark.parametrize(
    "text",
    ["collection,author\nBook,Writer\n", "collection,title\n,Story\n", "collection,title\nBook,\n"],
)
def test_invalid_csv(text: str, tmp_path: Path) -> None:
    path = write(tmp_path / "bad.csv", text)
    with pytest.raises(ValueError):
        load_csv(path)


def test_cli_outputs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = write(
        tmp_path / "stories.csv",
        "collection,title,author\nOne,Story,A\nTwo,Story,A\nThree,Story,B\n",
    )
    output = tmp_path / "map.json"
    assert main([str(path), "--json", str(output)]) == 1
    assert len(json.loads(output.read_text(encoding="utf-8"))["possible_collisions"]) == 1
    assert "Shared stories: 1" in capsys.readouterr().out
    assert "**Story**" in markdown(build_map(load_csv(path)))


def test_clean_cli_exit(tmp_path: Path) -> None:
    path = write(tmp_path / "stories.csv", "collection,title\nOne,Story\n")
    assert main([str(path)]) == 0
