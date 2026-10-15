# Short-Story Collection Mapper

Short-Story Collection Mapper turns a supplied CSV inventory into a reviewable map of stories shared across collections and stories exclusive to one collection. It prefers explicit identifiers, otherwise groups conservatively by normalized author and title, and surfaces same-title collisions instead of silently merging them.

## Three-minute use

Create `stories.csv`:

```csv
collection,title,author,identifier
Collected Tales,The Door,A. Writer,
Best of the Year,The Door,A. Writer,
Collected Tales,Only Here,A. Writer,
```

Then run:

```sh
python -m pip install "short-story-collection-mapper @ https://github.com/loganpendragonmultiverse/short-story-collection-mapper/releases/download/v1.1.1/short_story_collection_mapper-1.1.1-py3-none-any.whl"
story-collection-map stories.csv --markdown map.md --json map.json
```

## Privacy and limitations

The tool is local and never queries ISBN, ISFDB, publisher, or author databases. It cannot prove that retitled, translated, revised, or abridged stories are equivalent. Possible collisions require human review. Reports reproduce supplied bibliographic data, so review them before sharing.

## Development

```sh
python -m pip install -e ".[dev]"
ruff format --check . && ruff check .
mypy src tests
pytest
python -m build
```

Version 1.0.0 is feature complete for CSV inventories. Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md), security reports follow [SECURITY.md](SECURITY.md), and the project uses the MIT License.

## More open-source projects

This project is part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Browse the catalog for other released tools, source repositories, live demos, and downloads.


## Version 1.1.0

Compare two supplied collection labels with:

```bash
story-collection-map inventory.csv --compare "Collection A" "Collection B" --json comparison.json
```

The focused report contains `shared`, `only_left`, `only_right`, and possible title collisions. It uses exactly the global map's existing identifier-first grouping, including its conservative title/author fallback. Repeated rows do not create additional stories. Labels must match inventory collection names exactly, and selecting an unknown or identical pair fails clearly. Other collections do not influence the focused result. Omitting `--compare` retains the full map.
