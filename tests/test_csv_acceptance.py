from pathlib import Path

from short_story_collection_mapper.core import build_map, compare_collections, load_csv


def test_bom_quoted_csv_and_conservative_identities(tmp_path: Path) -> None:
    path = tmp_path / "inventory.csv"
    path.write_text(
        "\ufeffCollection,Title,Author,Identifier\n"
        'Left,"The, Door","A. Writer",shared-1\n'
        'Right,"Renamed\nStory",B. Writer,shared-1\n'
        "Left,Only here,C. Writer,\n"
        "Left,Only here,C. Writer,\n"
        "Other,The Door,D. Writer,different\n",
        encoding="utf-8",
    )
    before = path.read_bytes()
    rows = load_csv(path)
    assert len(rows) == 5
    whole = build_map(rows)
    assert whole.unique_story_count == 3
    focused = compare_collections(rows, "Left", "Right")
    assert len(focused.shared) == 1
    assert focused.shared[0].identifier == "shared-1"
    assert focused.shared[0].collections == ("Left", "Right")
    assert len(focused.only_left) == 1
    assert focused.only_right == ()
    assert path.read_bytes() == before
