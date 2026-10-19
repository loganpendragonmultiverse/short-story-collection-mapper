# Short-Story Collection Mapper

> ⭐ **Gold Star Project**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Map supplied story inventories and compare shared or exclusive stories across collections.

Short-Story Collection Mapper turns a supplied CSV inventory into a reviewable map of stories shared across collections and stories exclusive to one collection. It prefers explicit identifiers, otherwise groups conservatively by normalized author and title, and surfaces same-title collisions instead of silently merging them.

## Three-minute use

Requires Python 3.10 or newer, with no runtime dependencies.

Create `stories.csv`:

```csv
collection,title,author,identifier
Collected Tales,The Door,A. Writer,
Best of the Year,The Door,A. Writer,
Collected Tales,Only Here,A. Writer,
```

Then run:

```sh
python -m pip install "short-story-collection-mapper @ https://github.com/loganpendragonmultiverse/short-story-collection-mapper/releases/download/v1.1.2/short_story_collection_mapper-1.1.2-py3-none-any.whl"
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

## Version 1.1.2 — 2026-10-19

Report destinations must be new, distinct files, separate from every input. Existing files and symlink destinations are refused. Ordinary read, report-write and stdout failures return exit code 2. Inputs and existing reports are preserved. A later write failure can leave a partial new report or an already completed first report; inspect these paths and choose new names when retrying. Reports are not a multi-file or power-loss transaction.

Supported scope: Map supplied CSV story inventories, review shared and exclusive groups and compare two named collections. No external data is fetched and no source file is rewritten.

Authored names, values and titles are escaped in Markdown reports so pipes, backticks, line breaks and HTML text remain report content. JSON values are unchanged.
