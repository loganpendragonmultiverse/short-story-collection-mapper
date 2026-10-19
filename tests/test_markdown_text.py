from short_story_collection_mapper.cli import comparison_markdown, markdown
from short_story_collection_mapper.core import StoryRow, build_map, compare_collections


def test_authored_text_stays_inside_markdown_items() -> None:
    text = "Title**\n## Hidden <script>`|"
    rows = [StoryRow(text, text, text, text), StoryRow("Other", text, text, text)]
    full = build_map(rows)
    focused = compare_collections(rows, text, "Other")
    before = full.to_dict(), focused.to_dict()
    for rendered in [markdown(full), comparison_markdown(focused)]:
        assert "\n## Hidden" not in rendered
        assert "<script>" not in rendered
        assert "&#42;" in rendered and "&#96;" in rendered and "&#10;" in rendered
    assert (full.to_dict(), focused.to_dict()) == before
