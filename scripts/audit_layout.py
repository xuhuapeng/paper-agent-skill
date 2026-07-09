#!/usr/bin/env python3
"""Audit LaTeX layout defects that structural checks miss.

Usage:
  python audit_layout.py /path/to/paper_version [--threshold PT]

Structural audits (citations, figures, claims) cannot see VISUAL layout
defects such as an overfull \\hbox where a long unbreakable token spills
out of its column and overlaps neighbouring text. This script compiles the
manuscript with tectonic and reports every overfull box whose overflow is
large enough to be visible (default >= 12pt), so the reviewer knows exactly
which pages to render-and-inspect.

It uses only the Python standard library plus a local `tectonic` binary.
If tectonic is unavailable, it parses an existing build log instead.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

OVERFULL_RE = re.compile(
    r"Overfull \\hbox \(([0-9.]+)pt too wide\).*?(?:lines? (\d+)(?:--(\d+))?)?",
    re.IGNORECASE,
)


def find_main_tex(root: Path) -> Path | None:
    candidates = [root / "main.tex"]
    candidates += sorted(root.glob("*.tex"))
    for path in candidates:
        if path.is_file() and "\\documentclass" in path.read_text(
            encoding="utf-8", errors="ignore"
        ):
            return path
    return None


def get_build_log(root: Path, main_tex: Path) -> str:
    if shutil.which("tectonic"):
        proc = subprocess.run(
            ["tectonic", main_tex.name],
            cwd=root,
            capture_output=True,
            text=True,
        )
        return proc.stdout + proc.stderr
    log = main_tex.with_suffix(".log")
    if log.is_file():
        return log.read_text(encoding="utf-8", errors="ignore")
    return ""


def parse_overfull(log: str, threshold: float) -> list[tuple[float, str]]:
    hits: list[tuple[float, str]] = []
    seen: set[str] = set()
    for line in log.splitlines():
        match = OVERFULL_RE.search(line)
        if not match:
            continue
        pt = float(match.group(1))
        if pt < threshold:
            continue
        key = line.strip()
        if key in seen:
            continue
        seen.add(key)
        hits.append((pt, line.strip()))
    return sorted(hits, key=lambda x: -x[0])


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path.cwd().resolve()
    threshold = 12.0
    if "--threshold" in sys.argv:
        threshold = float(sys.argv[sys.argv.index("--threshold") + 1])

    if not root.exists():
        print(f"ERROR: root does not exist: {root}")
        return 2

    main_tex = find_main_tex(root)
    if not main_tex:
        print(f"ERROR: no main .tex with \\documentclass under {root}")
        return 2

    log = get_build_log(root, main_tex)
    if not log:
        print("ERROR: no build log and tectonic unavailable; compile first")
        return 2

    hits = parse_overfull(log, threshold)
    print(f"ROOT: {root}")
    print(f"MAIN_TEX: {main_tex.name}")
    print(f"OVERFULL_THRESHOLD_PT: {threshold}")
    print(f"VISIBLE_OVERFULL_BOXES: {len(hits)}")
    for pt, line in hits:
        print(f"  - {pt}pt :: {line}")
    if hits:
        print(
            "ACTION: render the affected pages to images and visually confirm "
            "whether any box overlaps neighbouring text before claiming layout clean."
        )
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
