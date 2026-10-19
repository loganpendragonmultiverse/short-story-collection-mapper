# Development record

Version 1.0.0 implements the complete initial scope: supplied CSV inventories, conservative grouping, collection membership maps, and collision review. External metadata lookup and automatic equivalence claims are excluded.


## Version 1.1.0

Compare two supplied collection labels with:

```bash
story-collection-map inventory.csv --compare "Collection A" "Collection B" --json comparison.json
```

The focused report contains `shared`, `only_left`, `only_right`, and possible title collisions. It uses exactly the global map's existing identifier-first grouping, including its conservative title/author fallback. Repeated rows do not create additional stories. Labels must match inventory collection names exactly, and selecting an unknown or identical pair fails clearly. Other collections do not influence the focused result. Omitting `--compare` retains the full map.

## 1.1.2 report reliability — 2026-10-19

Preserve source bytes and existing reports. Refuse source aliases, symlinks, duplicate report destinations and files that appear immediately before exclusive creation. Cover ordinary file/encoding/stdout failures and retry at a new path. Run formatting, lint, strict typing, the full coverage suite, builds and dependency audit. Install wheel and source distributions separately outside the source tree; exercise primary workflows and error paths. Independent review and required CI precede merge/release. Publish actual tag-built artifacts with SHA256 checksums after installed acceptance; Gold qualification follows verified publication and catalog reconciliation.
