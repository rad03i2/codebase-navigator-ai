# Roadmap

This file contains **possible future directions**. Nothing listed here should be interpreted as available in the current release.

The current v1.0 feature set is documented in [README.md](README.md).

## Near-term candidates

### Persistent local index

Avoid rebuilding the complete in-memory index for every CLI invocation by storing a local cache with clear invalidation rules.

Key constraints:

- local-only storage;
- explicit cache location;
- deterministic rebuild behavior;
- no source upload.

### Ignore-file support

Consider honoring project ignore files such as `.gitignore` in addition to the current built-in ignored directory names.

This requires careful semantics because ignore-file behavior can differ across tooling.

### Additional language structure

Potentially add parser-backed symbol discovery for languages beyond Python.

Any implementation should clearly distinguish:

- text-search support;
- syntax-aware symbol support;
- deeper semantic analysis.

## Longer-term exploration

### Cross-reference graph

Explore relationships such as references or imports without executing project code.

### Local semantic search

A future **optional** pluggable local backend could provide semantic retrieval.

If pursued, it should be:

- opt-in;
- clearly separated from deterministic search;
- explicit about model/runtime dependencies;
- capable of operating without uploading private source.

### Optional LLM assistant layer

The project name leaves room for a future assistant layer, but no such integration exists today.

A future design should make these boundaries explicit:

- what source/context is sent to the model;
- whether the model is local or remote;
- how users opt in;
- what credentials are required;
- how sensitive repositories are protected.

## Non-goals unless the project scope changes

- silently executing inspected code;
- hidden telemetry;
- implicit upload of repository contents;
- pretending text search is semantic AI search;
- presenting unsupported languages as structurally parsed.

## Guiding principle

Future intelligence should make navigation better **without making the trust boundary less clear**.
