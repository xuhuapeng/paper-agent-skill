---
name: paper-agent-skill
description: "Long-term LaTeX research-paper iteration skill. Use when reviewing, rewriting, or upgrading manuscripts across versions; enforcing a claim-evidence contract; auditing citations, BibTeX, figures, tables, and LaTeX; checking paper-code alignment and top-conference readiness; running rebuttal-style critique or an Iteration Review. Triggers: 论文修改, 论文迭代, paper review, paper rewrite, manuscript revision, citation audit, figure/table QA, claim-evidence matrix, top-conference review, Iteration Review."
---

# paper-agent-skill

## Purpose

Use this skill for serious, multi-round research-paper iteration. Treat each request as part of a versioned manuscript system. Do not claim hidden memory; recover context from the paper files, any project notes/reports, code, and the current manuscript artifacts.

## Quick Target Defaults

- Workspace root: `<workspace>` (the repo/folder that contains your paper)
- Paper root: `<workspace>/<paper-root>` (the directory holding your paper versions)
- Latest baseline before a new version: read `references/project-baseline.md`, any project notes, and the newest paper folder
- Durable reports: `<workspace>/<reports-dir>` (wherever you keep durable work reports)

Fill these placeholders in for your own project, and update them when a newer canonical version appears.

## Non-Negotiables

- No shallow polishing for core paper work. Fix the claim, evidence, and argument chain before improving prose.
- Do not invent citations, BibTeX metadata, venues, years, DOI/arXiv IDs, datasets, production lifts, or deployment status.
- Separate implemented work, public proxy experiments, proposed design, and future work.
- Keep speculative extensions (a not-yet-implemented tokenizer, loss, or module) in Future Work unless code, experiments, and manuscript evidence justify moving them into the method.
- Make Figure 1, the abstract, and the introduction agree before treating a structural rewrite as done.
- For major rewrites, create a new paper version unless the user explicitly asks to edit in place.
- For non-trivial paper work, compile/audit when feasible and write a concise durable work report.

## Progressive Resources

Read only the references needed for the task:

| Need | Load |
|---|---|
| Version recovery, rewrite modes, structural workflow | `references/manuscript-workflow.md` |
| Project baseline template + common LaTeX gotchas | `references/project-baseline.md` |
| Citation verification, literature routing, evidence tables | `references/citation-literature-workflow.md` |
| Figure/table design and LaTeX figure QA | `references/figure-table-protocol.md` |
| Layered verification + why audits miss defects | `references/verification-layers.md` |
| Top-conference checklist and reviewer simulation | `references/top-conference-review.md` |
| Final review report shape | `references/iteration-review-template.md` |

Use the scripts for deterministic checks:

```bash
python3 scripts/audit_latex_refs.py <paper_version_dir>
python3 scripts/audit_bib_metadata.py <paper_version_dir>
python3 scripts/audit_figures.py <paper_version_dir>
python3 scripts/audit_claim_language.py <paper_version_dir>
python3 scripts/audit_layout.py <paper_version_dir> --threshold 12
```

Use `evals/` as regression memory for known failure modes: citation hallucination, hidden figure bodies, overclaiming, and rendered-layout overlap.

## Operating Modes

### Mode A - Local Paper Patch

Use for small wording, citation, equation, caption, or table changes. Patch only affected files, preserve structure, run targeted validation, and report remaining risks.

### Mode B - Structural Manuscript Rewrite

Use when positioning, novelty, method logic, experiment logic, figure system, or citation quality changes. First lock the one-sentence contribution, Figure 1 reviewer question, claim-evidence matrix, evidence boundary, and version target. Then rewrite the manuscript, compile, run audits, and produce an Iteration Review.

### Mode C - Algorithm Or Architecture Change

Use when tokenizer, model graph, loss, training objective, serving logic, baseline, ablation, or experimental claim changes. Decide whether it is implemented, proxy, proposed, or future work. Align paper/code/runbook when feasible; otherwise downgrade the claim.

### Mode D - Review Or Strategy Memo

Use when the user asks for critique or strategy without source edits. Lead with findings and risks, separate paper-writing/research-design/experiment/implementation/prior-art defects, and give prioritized repair actions.

## Required Workflow

1. Recover context: project notes, latest paper version, reports, `main.tex`, sections, figures, refs, code/outputs if claims touch implementation.
2. Classify mode and target: source version, output version, edit/review scope, evidence boundary.
3. Build or update a claim-evidence matrix for serious rewrites.
4. Verify citations with local `.bib` and external/public sources when adding or judging references; mark unresolved items explicitly.
5. Validate figure/table artifacts: existence, caption, label, `\Description{}`, referenced labels, rendering for high-risk figures.
6. Compile LaTeX with `tectonic main.tex` when available.
7. Run available audit scripts and interpret advisory warnings rather than blindly treating every warning as fatal.
8. Run the layered verification in `references/verification-layers.md`. A clean compile and green source audits are necessary but not sufficient: also run the layout audit and **render-and-inspect** flagged pages (L5), and manually check table headers, axis labels, and captions for proxy-as-real or semantic drift (L6). State in the report which layers were actually run.
9. Write an Iteration Review for Mode B/C.
10. Update your durable work report/log and any project notes when the canonical version or validated status changes.

## Default Evidence Stance

Set this per project and refresh it after each serious iteration. A sound default:

- State the paper's current identity honestly (for example, a system/architecture contract or a method study) rather than as a production-lift claim, unless you have production evidence.
- Name which components are the currently deployable/validated contract versus which are only proposed.
- Keep any not-yet-implemented extension in future work until it is implemented and evaluated.
- Treat evidence as synthetic/proxy unless the user supplies real logs, production A/B evidence, or validated private artifacts.
- Default to RecSys/CIKM/WWW industry-track rigor unless the user specifies NeurIPS/ICML or another venue.

Refresh this stance after each serious paper iteration.
