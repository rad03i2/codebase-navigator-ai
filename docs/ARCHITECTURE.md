# Codebase Navigator AI Architecture

This document describes the **current v1.0 implementation**. It does not describe roadmap features as if they already exist.

## Component map

| Component | Current responsibility |
|---|---|
| `src/codebase_navigator/core.py` | Repository discovery, file filtering, Python AST symbols, text/regex search, source context |
| `src/codebase_navigator/cli.py` | CLI parsing, subcommands, human/JSON rendering, user-facing error handling |
| `src/codebase_navigator/__init__.py` | Public Python API and package version |
| `tests/test_core.py` | Functional unit coverage for indexing, search, symbols, context, and validation |
| `.github/workflows/ci.yml` | Cross-platform compile, test, and CLI smoke checks |

## Data model

### `Symbol`

A discovered Python structural symbol:

- `name`
- `kind`
- `path`
- `line`
- `signature`

Current kinds are `class`, `function`, and `async-function`.

### `Match`

A text-search result:

- relative path;
- 1-based line number;
- trimmed line text.

### `Index`

The in-memory repository map:

- resolved root path;
- indexed files;
- discovered Python symbols;
- skipped-file count.

The CLI rebuilds this index for every invocation.

## Index construction

```text
build_index(root)
      │
      ▼
resolve root
      │
      ├─ reject non-directory roots
      ├─ validate positive limits
      │
      ▼
root.rglob("*")
      │
      ├─ skip symlinks
      ├─ keep files only
      ├─ skip ignored path components
      ├─ filter by supported suffix
      ├─ enforce max_files
      ├─ skip files above max_bytes
      └─ read UTF-8 text
      │
      ├───────────────┐
      ▼               ▼
index file        .py file?
                       │
                       ▼
                   ast.parse
                       │
                       ├─ SyntaxError → no symbols
                       └─ walk AST → classes/functions
```

Unreadable or non-UTF-8 files increment the skipped counter and are not indexed.

## Default boundaries

### File-count limit

`max_files=20_000`

Once the number of accepted files reaches the limit, the next eligible file causes a `RuntimeError`.

### File-size limit

`max_bytes=1_000_000`

Files above this size are skipped and counted in `skipped`.

### Ignored path components

```text
.git
.venv
venv
node_modules
dist
build
__pycache__
.pytest_cache
```

The API can supply a different `ignores` iterable.

## Python symbol extraction

`_python_symbols(...)` parses source with the standard-library `ast` module.

It discovers:

- `ast.ClassDef`
- `ast.FunctionDef`
- `ast.AsyncFunctionDef`

The implementation walks the entire AST, so nested definitions can also be discovered. Results are sorted by relative path and line.

A syntax error causes symbol extraction for that file to return an empty list. The file can still remain in the index for text search.

## Text and regex search

`search_text(...)`:

1. rejects an empty query;
2. optionally compiles a case-insensitive regex;
3. filters relative paths through `fnmatch`;
4. rereads each selected indexed file as UTF-8;
5. evaluates each line;
6. returns a `Match` with line text trimmed to the implementation's preview cap.

Invalid regex errors are allowed to propagate to the CLI's controlled error handling.

## Focused context

`context(...)`:

1. validates line and radius;
2. resolves `index.root / path`;
3. verifies the resolved path remains under the indexed root;
4. verifies the target belongs to the current index;
5. returns the requested line window.

This is the main path-traversal boundary for targeted source reading.

## CLI surface

Current subcommands:

- `summary`
- `symbols`
- `search`
- `context`

Global options:

- `--root`
- `--json`
- `--version`

The CLI catches `ValueError`, `RuntimeError`, and regex errors, prints a concise error to stderr, and returns exit code 2.

## Trust boundary

The tool does **not** intentionally:

- execute inspected source;
- import inspected modules;
- follow symlinks;
- transmit source over the network;
- require API credentials.

The package itself currently declares no runtime third-party dependency.

These boundaries reduce exposure but do not classify a repository as safe. Codebase Navigator AI is not a malware scanner or sandbox.

## CI contract

The current GitHub Actions matrix uses Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

Each job runs:

```bash
python -m pip install -e .
python -m compileall -q src tests
python -m unittest discover -s tests -v
codebase-nav --root . summary
```
