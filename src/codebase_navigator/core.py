from __future__ import annotations

import ast
import fnmatch
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

DEFAULT_IGNORES = (".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".pytest_cache")
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".c", ".h", ".cpp", ".cs", ".rb", ".php", ".md", ".toml", ".yaml", ".yml", ".json", ".txt"}

@dataclass(frozen=True)
class Symbol:
    name: str
    kind: str
    path: str
    line: int
    signature: str = ""

@dataclass(frozen=True)
class Match:
    path: str
    line: int
    text: str

@dataclass
class Index:
    root: Path
    files: list[Path]
    symbols: list[Symbol]
    skipped: int = 0

    def summary(self) -> dict:
        return {"root": str(self.root), "files": len(self.files), "symbols": len(self.symbols), "skipped": self.skipped}

    def to_dict(self) -> dict:
        return {**self.summary(), "symbols": [asdict(s) for s in self.symbols]}


def _ignored(path: Path, root: Path, ignores: Iterable[str]) -> bool:
    rel = path.relative_to(root)
    return any(part in ignores for part in rel.parts)


def _signature(node: ast.AST) -> str:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = [a.arg for a in node.args.posonlyargs + node.args.args]
        if node.args.vararg: args.append("*" + node.args.vararg.arg)
        args += [a.arg for a in node.args.kwonlyargs]
        if node.args.kwarg: args.append("**" + node.args.kwarg.arg)
        return f"{node.name}({', '.join(args)})"
    return getattr(node, "name", "")


def _python_symbols(path: Path, root: Path, text: str) -> list[Symbol]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    out: list[Symbol] = []
    rel = path.relative_to(root).as_posix()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            out.append(Symbol(node.name, "class", rel, node.lineno, node.name))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = "async-function" if isinstance(node, ast.AsyncFunctionDef) else "function"
            out.append(Symbol(node.name, kind, rel, node.lineno, _signature(node)))
    return sorted(out, key=lambda s: (s.path, s.line))


def build_index(root: str | Path, *, max_files: int = 20000, max_bytes: int = 1_000_000, ignores: Iterable[str] = DEFAULT_IGNORES) -> Index:
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    if max_files < 1 or max_bytes < 1:
        raise ValueError("max_files and max_bytes must be positive")
    files: list[Path] = []
    symbols: list[Symbol] = []
    skipped = 0
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or _ignored(path, root, ignores):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if len(files) >= max_files:
            raise RuntimeError(f"File limit exceeded ({max_files})")
        try:
            if path.stat().st_size > max_bytes:
                skipped += 1; continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            skipped += 1; continue
        files.append(path)
        if path.suffix.lower() == ".py":
            symbols.extend(_python_symbols(path, root, text))
    return Index(root, sorted(files), symbols, skipped)


def find_symbols(index: Index, query: str, *, kind: str | None = None) -> list[Symbol]:
    q = query.casefold()
    return [s for s in index.symbols if q in s.name.casefold() and (kind is None or s.kind == kind)]


def search_text(index: Index, query: str, *, regex: bool = False, glob: str = "*") -> list[Match]:
    if not query:
        raise ValueError("query must not be empty")
    pattern = re.compile(query, re.IGNORECASE) if regex else None
    out: list[Match] = []
    for path in index.files:
        rel = path.relative_to(index.root).as_posix()
        if not fnmatch.fnmatch(rel, glob):
            continue
        try: lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError): continue
        for n, line in enumerate(lines, 1):
            if (pattern.search(line) if pattern else query.casefold() in line.casefold()):
                out.append(Match(rel, n, line.strip()[:300]))
    return out


def context(index: Index, path: str, line: int, radius: int = 3) -> list[tuple[int, str]]:
    if line < 1 or radius < 0: raise ValueError("invalid line/radius")
    target = (index.root / path).resolve()
    try: target.relative_to(index.root)
    except ValueError: raise ValueError("path escapes project root") from None
    if target not in index.files: raise ValueError("path is not an indexed file")
    lines = target.read_text(encoding="utf-8").splitlines()
    start, end = max(1, line-radius), min(len(lines), line+radius)
    return [(n, lines[n-1]) for n in range(start, end+1)]
