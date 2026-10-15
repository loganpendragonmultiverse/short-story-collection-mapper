import json
from pathlib import Path

import pytest

from short_story_collection_mapper.cli import main
from short_story_collection_mapper.core import StoryRow, build_map, compare_collections


def rows() -> list[StoryRow]:
    return [
        StoryRow("Left", "Shared", "A", "id1"),
        StoryRow("Right", "Renamed", "B", "id1"),
        StoryRow("Left", "Collision", "A", "x"),
        StoryRow("Right", "Collision", "B", "y"),
        StoryRow("Left", "Alone"),
        StoryRow("Left", "Alone"),
        StoryRow("Third", "Shared", "A", "id1"),
        StoryRow("Third", "Third only"),
    ]


def test_focused_identity_and_collisions() -> None:
    source = rows()
    before = build_map(source)
    result = compare_collections(source, "Left", "Right")
    assert len(result.shared) == 1
    assert result.shared[0].identifier == "id1"
    assert result.shared[0].collections == ("Left", "Right")
    assert len(result.only_left) == 2
    assert len(result.only_right) == 1
    assert len(result.possible_collisions) == 1
    assert build_map(source) == before
    assert before.collection_count == 3
    assert result.to_dict()["left"] == "Left"
    for left, right in (("Left", "Left"), ("Left", "Unknown"), ("left", "Right")):
        with pytest.raises(ValueError):
            compare_collections(source, left, right)


def test_cli_comparison(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "stories.csv"
    source.write_text(
        "collection,title,author,identifier\nLeft,One,A,s1\nRight,One,A,s1\nRight,Two,B,s2\n"
    )
    output = tmp_path / "result.json"
    assert main([str(source), "--compare", "Left", "Right", "--json", str(output)]) == 0
    assert len(json.loads(output.read_text())["shared"]) == 1
    rendered = capsys.readouterr().out
    assert "Only left" in rendered and "Only right" in rendered
    with pytest.raises(SystemExit):
        main([str(source), "--compare", "Left", "missing"])
