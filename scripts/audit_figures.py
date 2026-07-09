#!/usr/bin/env python3
"""Audit LaTeX figure inclusion health for a paper version directory.

Usage:
  python audit_figures.py /path/to/paper_version

Checks included figure paths, asset existence, caption/label/Description
presence in simple figure environments, and high-risk PDF-vs-PNG cases.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

INCLUDE_RE = re.compile(r"\\(?:includegraphics|includefigure)(?:\[[^\]]*\])?\{([^}]+)\}")
FIG_ENV_RE = re.compile(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", re.S)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def resolve_asset(root: Path, figure_path: str) -> tuple[bool, list[Path]]:
    raw = Path(figure_path)
    candidates = []
    if raw.suffix:
        candidates.append(root / raw)
    else:
        candidates.extend(root / f"{figure_path}{suffix}" for suffix in (".png", ".pdf", ".jpg", ".jpeg", ".svg"))
    existing = [path for path in candidates if path.exists() and path.is_file()]
    return bool(existing), existing


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    tex_files = sorted(root.rglob("*.tex"))
    missing_assets: list[str] = []
    empty_assets: list[str] = []
    pdf_png_pairs: list[str] = []
    env_issues: list[str] = []

    for tex in tex_files:
        text = read(tex)
        for match in INCLUDE_RE.finditer(text):
            figure_path = match.group(1)
            if figure_path.startswith('#'):
                continue
            ok, existing = resolve_asset(root, figure_path)
            if not ok:
                missing_assets.append(f"{tex}: {figure_path}")
                continue
            for path in existing:
                if path.stat().st_size == 0:
                    empty_assets.append(str(path))
            stem = root / figure_path
            if not Path(figure_path).suffix and stem.with_suffix('.pdf').exists() and stem.with_suffix('.png').exists():
                pdf_png_pairs.append(figure_path)

        for env_no, env in enumerate(FIG_ENV_RE.findall(text), 1):
            if "\\caption" not in env:
                env_issues.append(f"{tex}: figure env {env_no} missing caption")
            if "\\label" not in env:
                env_issues.append(f"{tex}: figure env {env_no} missing label")
            if "\\Description" not in env:
                env_issues.append(f"{tex}: figure env {env_no} missing Description")

    print(f"ROOT: {root}")
    print(f"TEX_FILES: {len(tex_files)}")
    print(f"MISSING_ASSETS: {len(missing_assets)}")
    for item in missing_assets:
        print(f"  - {item}")
    print(f"EMPTY_ASSETS: {len(empty_assets)}")
    for item in empty_assets:
        print(f"  - {item}")
    print(f"PDF_PNG_PAIRS: {len(pdf_png_pairs)}")
    for item in sorted(set(pdf_png_pairs)):
        print(f"  - {item} (ensure macro intentionally chooses PNG or clean vector PDF)")
    print(f"FIGURE_ENV_ISSUES: {len(env_issues)}")
    for item in env_issues:
        print(f"  - {item}")

    return 1 if missing_assets or empty_assets or env_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
