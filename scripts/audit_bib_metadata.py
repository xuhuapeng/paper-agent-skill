#!/usr/bin/env python3
"""Lightweight BibTeX metadata audit for paper version directories.

Usage:
  python audit_bib_metadata.py /path/to/paper_version

This script intentionally uses only the Python standard library. It does not
verify metadata against Crossref/Semantic Scholar; it flags entries that need
human/API verification before submission.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}\s*", re.S)
FIELD_RE = re.compile(r"\n\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[\{\"]", re.S)
SUSPICIOUS_RE = re.compile(r"PLACEHOLDER|TODO|VERIFY|citation needed|unknown|tbd", re.I)
ARXIV_RE = re.compile(r"arXiv:\s*\d{4}\.\d{4,5}|eprint\s*=\s*[\{\"]\d{4}\.\d{4,5}", re.I)
DOI_RE = re.compile(r"doi\s*=\s*[\{\"][^\}\"]+", re.I)

REQUIRED_COMMON = {"author", "title", "year"}
VENUE_FIELDS = {"journal", "booktitle", "publisher", "archiveprefix", "eprint"}


def parse_entries(path: Path) -> list[tuple[str, str, str, set[str]]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    entries = []
    for entry_type, key, body in ENTRY_RE.findall(text):
        fields = {name.lower() for name in FIELD_RE.findall("\n" + body)}
        entries.append((entry_type.lower(), key, body, fields))
    return entries


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    bib_files = sorted(root.rglob("*.bib"))
    issues: list[str] = []
    entries_seen = 0

    for bib in bib_files:
        entries = parse_entries(bib)
        entries_seen += len(entries)
        keys: set[str] = set()
        for entry_type, key, body, fields in entries:
            if key in keys:
                issues.append(f"{bib}: duplicate key in same file: {key}")
            keys.add(key)

            missing = sorted(REQUIRED_COMMON - fields)
            if missing:
                issues.append(f"{bib}: {key}: missing required fields {', '.join(missing)}")
            if not (fields & VENUE_FIELDS):
                issues.append(f"{bib}: {key}: missing venue/source field (journal/booktitle/publisher/archiveprefix/eprint)")
            if not (DOI_RE.search(body) or ARXIV_RE.search(body) or "url" in fields):
                issues.append(f"{bib}: {key}: no DOI, arXiv/eprint, or URL field for external verification")
            if SUSPICIOUS_RE.search(body):
                issues.append(f"{bib}: {key}: contains placeholder-like text")
            if entry_type in {"misc", "online"} and "howpublished" not in fields and "url" not in fields and "eprint" not in fields:
                issues.append(f"{bib}: {key}: weak misc/online entry without howpublished/url/eprint")

    print(f"ROOT: {root}")
    print(f"BIB_FILES: {len(bib_files)}")
    print(f"BIB_ENTRIES: {entries_seen}")
    print(f"METADATA_ISSUES: {len(issues)}")
    for issue in issues[:120]:
        print(f"  - {issue}")
    if len(issues) > 120:
        print(f"  ... {len(issues) - 120} more")

    # Advisory only: metadata gaps are common in drafts and should not fail builds.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
