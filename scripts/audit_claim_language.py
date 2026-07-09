#!/usr/bin/env python3
"""Scan paper text for overclaiming phrases that need evidence boundaries.

Usage:
  python audit_claim_language.py /path/to/paper_version
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Project-specific: names of not-yet-implemented extensions your paper must NOT
# present as done (e.g. "the new tokenizer", "the online learner"). Leave empty to disable.
PROJECT_EXTENSION_TERMS: list[str] = []

PATTERNS = [
    ("production_lift", re.compile(r"production (online )?lift|online A/B|A/B test", re.I)),
    ("sota", re.compile(r"state[- ]of[- ]the[- ]art|SOTA|outperform[s]? all|best performance", re.I)),
    ("causal", re.compile(r"causal|unbiased propensity|true propensity", re.I)),
    ("absolute", re.compile(r"\bguarantee[s]?\b|\bprove[s]?\b|\beliminate[s]?\b|\balways\b|\bnever\b", re.I)),
]

# Opt-in: flag each project extension term claimed as implemented without a boundary.
for _term in PROJECT_EXTENSION_TERMS:
    PATTERNS.append(
        (
            f"extension_claimed_implemented:{_term}",
            re.compile(
                rf"{re.escape(_term)}(?![^.]{{0,120}}(future|Future|planned|unimplemented|not implemented))",
                re.I,
            ),
        )
    )

BOUNDARY_RE = re.compile(
    r"does not claim|does not prove|does not support|does not validate|not claim|"
    r"do not claim|do not prove|do not support|do not validate|"
    r"not a causal|not causal|future work|future versions|outside|outside the present|"
    r"stronger claims|stronger causal claims|not the present evidence|no production",
    re.I,
)


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    hits: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*.tex")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        previous = ""
        for line_no, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('%'):
                previous = stripped
                continue
            context = f"{previous} {stripped}"
            if BOUNDARY_RE.search(context):
                previous = stripped
                continue
            for name, pattern in PATTERNS:
                if pattern.search(stripped):
                    hits.append((name, f"{path}:{line_no}: {stripped}"))
            previous = stripped

    print(f"ROOT: {root}")
    print(f"OVERCLAIM_CANDIDATES: {len(hits)}")
    for name, hit in hits:
        print(f"  - [{name}] {hit}")

    # This is advisory. Return 0 so known bounded mentions do not fail builds.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
