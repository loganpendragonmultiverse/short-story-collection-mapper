# Development record

Version 1.0.0 implements the complete initial scope: supplied CSV inventories, conservative grouping, collection membership maps, and collision review. External metadata lookup and automatic equivalence claims are excluded.


## Version 1.1.0

Compare two supplied collection labels with:

```bash
story-collection-map inventory.csv --compare "Collection A" "Collection B" --json comparison.json
```

The focused report contains `shared`, `only_left`, `only_right`, and possible title collisions. It uses exactly the global map's existing identifier-first grouping, including its conservative title/author fallback. Repeated rows do not create additional stories. Labels must match inventory collection names exactly, and selecting an unknown or identical pair fails clearly. Other collections do not influence the focused result. Omitting `--compare` retains the full map.
