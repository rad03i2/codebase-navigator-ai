# Changelog

All notable repository changes are recorded here.

The current package version is declared in `pyproject.toml`.

## Unreleased

### Repository experience

- Added a dedicated **Code Atlas** visual identity.
- Added a repository hero cover and square project logo.
- Reorganized the root README around the real v1.0 navigation workflow.
- Added separate English and Arabic documentation.
- Added architecture and brand documentation.
- Added a roadmap that clearly separates future AI ideas from current deterministic features.
- Added issue and pull-request templates.
- Expanded contribution and security documentation.

No runtime behavior was changed by these repository-presentation updates.

## 1.0.0

Current functional baseline:

- recursive local indexing of supported text/source files;
- common vendor/build-directory ignores;
- Python class, function, and async-function discovery through AST;
- compact Python signatures;
- case-insensitive literal search;
- opt-in regex search;
- path glob filtering;
- focused source context with root traversal protection;
- human-readable and JSON CLI output;
- small importable Python API;
- no runtime third-party dependencies;
- cross-platform CI on Python 3.10, 3.12, and 3.13.
