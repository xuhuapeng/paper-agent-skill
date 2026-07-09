# Manuscript Workflow Reference

## Mode Selection

Use the smallest mode that covers the request.

| Mode | Use when | Required output |
|---|---|---|
| Local Patch | small wording, citation, equation, caption, or table change | patched files + targeted validation |
| Structural Rewrite | positioning, innovation, argument chain, method/experiment logic, citation quality, or figure system changes | new version when appropriate + compile + iteration review |
| Algorithm / Architecture Change | tokenizer, model graph, loss, training, serving, baseline, ablation, or experimental claim changes | paper/code alignment decision + evidence boundary |
| Review Memo | critique, strategy, readiness, or next-step planning without source edits | findings first + prioritized repair path |

## Phase 0 Context Recovery

Before substantive edits:

1. Classify the request.
2. Read repo memory and current paper version evidence.
3. Inspect latest version directory, `main.tex`, sections, figures, refs, and build status.
4. Read affected sections before editing.
5. If claims touch code or experiments, inspect relevant code/output artifacts.
6. If citations change, identify active `.bib` and verification status.
7. State target briefly: source version, output version, mode, and evidence boundary.

Ask only when missing information changes the target or makes edits unsafe.

## Structural Rewrite Chain

For serious rewrites, lock these before prose polish:

1. One-sentence contribution.
2. Figure 1 reviewer question.
3. Claim-evidence matrix.
4. Method components and their failure modes.
5. Experiment questions and ablations.
6. Limitations/future-work boundary.
7. Title/abstract/introduction alignment.

## Versioning Rule

Create a new independent version for major rewrites unless the user asks to edit in place. Preserve prior versions for rollback.

## Build and Audit Minimum

For LaTeX papers:

- run `tectonic main.tex` when available
- check for fatal errors, undefined references/citations, missing figures, stale version labels
- run available skill scripts under `scripts/`
- if figures changed, render or inspect the PDF pages when feasible

## Durable Writeback

For non-trivial paper work, create or update a durable work report/log and any project notes, and state which validation layers were run and what remains unverified.