#!/usr/bin/env python3
"""Audit LaTeX citation keys against a BibTeX file.

Usage:
  python audit_latex_refs.py /path/to/paper_version

The script uses only the Python standard library. It reports missing
citation keys, unused BibTeX entries, unresolved placeholders, and stale
version labels that commonly survive paper-version rewrites.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")
PLACEHOLDER_RE = re.compile(r"PLACEHOLDER_VERIFY|\[CITATION NEEDED\]|TODO_CITE|citation needed", re.IGNORECASE)


def collect_tex_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.tex") if path.is_file())


def collect_cites(tex_files: list[Path]) -> dict[str, list[str]]:
    cites: dict[str, list[str]] = {}
    for path in tex_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in CITE_RE.finditer(text):
            for raw_key in match.group(1).split(','):
                key = raw_key.strip()
                if key:
                    cites.setdefault(key, []).append(str(path))
    return cites


def collect_bib_keys(root: Path) -> set[str]:
    keys: set[str] = set()
    for path in sorted(root.rglob("*.bib")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        keys.update(BIB_RE.findall(text))
    return keys


TITLE_RE = re.compile(r"title\s*=\s*[{\"]+(.+?)[}\"]+\s*,", re.IGNORECASE | re.DOTALL)


def _normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def collect_bib_entries(root: Path) -> list[tuple[str, str, str]]:
    """Return (key, normalized_title, source_path) for each bib entry."""
    entries: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*.bib")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for chunk in re.split(r"(?=@\w+\s*\{)", text):
            key_match = BIB_RE.match(chunk.strip())
            if not key_match:
                continue
            key = key_match.group(1).strip()
            title_match = TITLE_RE.search(chunk)
            title = _normalize_title(title_match.group(1)) if title_match else ""
            entries.append((key, title, str(path)))
    return entries


def find_duplicate_titles(entries: list[tuple[str, str, str]]) -> list[list[str]]:
    """Group keys whose normalized titles match (likely duplicate references)."""
    by_title: dict[str, list[str]] = {}
    for key, title, _ in entries:
        if title:
            by_title.setdefault(title, []).append(key)
    return [sorted(keys) for keys in by_title.values() if len(keys) > 1]


def find_placeholders(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                hits.append(f"{path}:{line_no}: {line.strip()}")
    return hits


def find_stale_labels(paths: list[Path], version: str | None) -> list[str]:
    if not version:
        return []
    stale = []
    current = re.escape(version)
    pattern = re.compile(r"([A-Za-z][\w-]*-[Vv]\d+|fig:v\d+_|eq:v\d+_|tab:v\d+_)")
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), 1):
            if pattern.search(line) and not re.search(current, line, flags=re.IGNORECASE):
                stale.append(f"{path}:{line_no}: {line.strip()}")
    return stale


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not root.exists():
        print(f"ERROR: root does not exist: {root}")
        return 2

    tex_files = collect_tex_files(root)
    bib_keys = collect_bib_keys(root)
    cites = collect_cites(tex_files)
    missing = sorted(set(cites) - bib_keys)
    unused = sorted(bib_keys - set(cites))
    duplicate_groups = find_duplicate_titles(collect_bib_entries(root))

    version_match = re.search(r"paper_v(\d+)", str(root))
    current_version = f"v{version_match.group(1)}" if version_match else None
    placeholders = find_placeholders(tex_files + sorted(root.rglob("*.bib")))
    stale = find_stale_labels(tex_files, current_version)

    print(f"ROOT: {root}")
    print(f"TEX_FILES: {len(tex_files)}")
    print(f"CITE_KEYS_USED: {len(cites)}")
    print(f"BIB_KEYS_DEFINED: {len(bib_keys)}")
    print(f"MISSING_CITES: {len(missing)}")
    for key in missing:
        print(f"  - {key} used in {', '.join(sorted(set(cites[key])))}")
    print(f"UNUSED_BIB_KEYS: {len(unused)}")
    for key in unused[:80]:
        print(f"  - {key}")
    if len(unused) > 80:
        print(f"  ... {len(unused) - 80} more")
    print(f"DUPLICATE_BIB_TITLES: {len(duplicate_groups)}")
    for group in duplicate_groups:
        print(f"  - same title: {', '.join(group)}")
    print(f"PLACEHOLDERS: {len(placeholders)}")
    for hit in placeholders:
        print(f"  - {hit}")
    print(f"STALE_VERSION_LABELS: {len(stale)}")
    for hit in stale[:80]:
        print(f"  - {hit}")
    if len(stale) > 80:
        print(f"  ... {len(stale) - 80} more")

    return 1 if missing or placeholders or stale or duplicate_groups else 0


if __name__ == "__main__":
    raise SystemExit(main())
