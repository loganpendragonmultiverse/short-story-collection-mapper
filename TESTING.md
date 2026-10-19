# Testing

## Feature-wave regression gate

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build` after installing `.[dev]` in an isolated environment. The focused regressions are in `tests/test_feature_wave.py`; run them together with the existing suite. Keep the configured coverage threshold. Repository CI supplies the supported OS/Python matrix.

## 1.1.2 report reliability — 2026-10-19

Preserve source bytes and existing reports. Refuse source aliases, symlinks, duplicate report destinations and files that appear immediately before exclusive creation. Cover ordinary file/encoding/stdout failures and retry at a new path. Run formatting, lint, strict typing, the full coverage suite, builds and dependency audit. Install wheel and source distributions separately outside the source tree; exercise primary workflows and error paths. Independent review and required CI precede merge/release. Publish actual tag-built artifacts with SHA256 checksums after installed acceptance; Gold qualification follows verified publication and catalog reconciliation.
