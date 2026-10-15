"""CSV ingestion and collection mapping."""

from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class StoryRow:
    """One supplied story appearance."""

    collection: str
    title: str
    author: str = ""
    identifier: str = ""


@dataclass(frozen=True)
class Story:
    """One normalized story and all collection appearances."""

    title: str
    author: str
    identifier: str
    collections: tuple[str, ...]


@dataclass(frozen=True)
class Collision:
    """Same normalized title attached to multiple authors or identifiers."""

    normalized_title: str
    labels: tuple[str, ...]


@dataclass(frozen=True)
class StoryMap:
    """Complete mapping result."""

    source_rows: int
    collection_count: int
    unique_story_count: int
    shared: tuple[Story, ...]
    exclusive: tuple[Story, ...]
    possible_collisions: tuple[Collision, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready representation."""
        return asdict(self)


def normalize(value: str) -> str:
    """Normalize display text for cautious exact grouping."""
    folded = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.sub(r"[^\w]+", " ", folded).split())


def load_csv(path: Path) -> list[StoryRow]:
    """Load collection, title, optional author, and optional identifier columns."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = {field.casefold(): field for field in (reader.fieldnames or [])}
        if not {"collection", "title"}.issubset(fields):
            raise ValueError("CSV requires collection and title columns")
        rows: list[StoryRow] = []
        for number, raw in enumerate(reader, start=2):
            collection = (raw.get(fields["collection"]) or "").strip()
            title = (raw.get(fields["title"]) or "").strip()
            if not collection or not title:
                raise ValueError(f"row {number} requires collection and title")
            author_field = fields.get("author")
            identifier_field = fields.get("identifier")
            rows.append(
                StoryRow(
                    collection,
                    title,
                    (raw.get(author_field) or "").strip() if author_field else "",
                    (raw.get(identifier_field) or "").strip() if identifier_field else "",
                )
            )
    return rows


def story_key(row: StoryRow) -> str:
    """Build a conservative grouping key, preferring an explicit identifier."""
    if row.identifier:
        return f"id:{normalize(row.identifier)}"
    return f"text:{normalize(row.author)}|{normalize(row.title)}"


def build_map(rows: list[StoryRow]) -> StoryMap:
    """Group appearances and surface title collisions for human review."""
    grouped: dict[str, list[StoryRow]] = {}
    title_keys: dict[str, set[str]] = {}
    for row in rows:
        key = story_key(row)
        grouped.setdefault(key, []).append(row)
        title_keys.setdefault(normalize(row.title), set()).add(key)
    stories: list[Story] = []
    for appearances in grouped.values():
        first = appearances[0]
        collections = tuple(sorted({item.collection for item in appearances}, key=str.casefold))
        stories.append(Story(first.title, first.author, first.identifier, collections))
    stories.sort(key=lambda item: (normalize(item.title), normalize(item.author)))
    collisions = tuple(
        Collision(title, tuple(sorted(keys)))
        for title, keys in sorted(title_keys.items())
        if len(keys) > 1
    )
    return StoryMap(
        source_rows=len(rows),
        collection_count=len({row.collection for row in rows}),
        unique_story_count=len(stories),
        shared=tuple(story for story in stories if len(story.collections) > 1),
        exclusive=tuple(story for story in stories if len(story.collections) == 1),
        possible_collisions=collisions,
    )


@dataclass(frozen=True)
class CollectionComparison:
    """Focused comparison using the same identities as the full map."""

    left: str
    right: str
    shared: tuple[Story, ...]
    only_left: tuple[Story, ...]
    only_right: tuple[Story, ...]
    possible_collisions: tuple[Collision, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def compare_collections(rows: list[StoryRow], left: str, right: str) -> CollectionComparison:
    """Compare two exact supplied collection labels without guessing equivalence."""
    collections = {row.collection for row in rows}
    if left == right:
        raise ValueError("choose two different collections")
    if left not in collections or right not in collections:
        raise ValueError("unknown collection; use an exact inventory collection label")
    focused = build_map([row for row in rows if row.collection in {left, right}])
    return CollectionComparison(
        left,
        right,
        focused.shared,
        tuple(story for story in focused.exclusive if left in story.collections),
        tuple(story for story in focused.exclusive if right in story.collections),
        focused.possible_collisions,
    )
