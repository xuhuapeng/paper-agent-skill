# Project Baseline (template)

A per-project baseline the agent reads before a new paper version. Copy this file,
fill in the placeholders for your own manuscript, and verify against the actual
workspace files before relying on it. Nothing here should be trusted as memory —
it is a checklist you keep current.

## Current Canonical State (fill in)

- Workspace root: `<workspace>`
- Paper root: `<workspace>/<paper-root>`
- Latest known version: `<paper_vN>` (the newest compiling version directory)
- Durable reports: `<workspace>/<reports-dir>`
- Project notes / memory: `<where you keep durable project notes>`

## Current Technical Positioning (fill in)

State, in two or three lines, what the paper currently *is* and is *not*. Keep it
honest about the evidence boundary. A worked example for a generative-recommendation
paper (yours will differ):

> The manuscript is a claim-evidence contract for an exposure-aware Semantic-ID
> recommender, not a production-lift claim. It connects an offline tokenizer
> (e.g. residual-quantized k-means), an online sequence encoder with multi-task
> routing, autoregressive ID decoding, exposure/reachability supervision, utility
> heads (CTR/CVR/CTCVR), a detached exposure residual, and dynamic top-K serving.

Replace the example with your own architecture. The point is that every noun here
should map to a real method component and a figure/table, or be cut.

## Evidence Boundaries (fill in)

- Which component is the currently deployable/validated contract.
- Which extension is future work until implemented and evaluated.
- Whether evidence is synthetic/proxy or backed by real data / production A/B.
- Claims you must NOT make without artifacts: production online lift, real-data
  SOTA, causal estimation, or "completed" work that is not implemented.

## Common LaTeX Gotchas (reusable, not project-specific)

These are generic and worth keeping across projects:

- `acmart` row coloring must load `\PassOptionsToPackage{table}{xcolor}` *before*
  `\documentclass`.
- For cropped raster figures, have the include macro prefer PNG over a same-stem
  PDF; raster-to-PDF wrappers can render as blank/hidden figure bodies inside
  `acmart` floats while the caption still shows.
- Keep figure crop boxes and the Figure 1 asset documented in the paper version's
  own `figures/README.md`, and make sure the artwork carries no stale version
  title baked into the image.
- Build command: `tectonic main.tex` from the paper version directory.
- Keep the version's source-of-truth artifacts (e.g. a `claim_evidence_matrix.md`
  and a `paper_manifest.json`) inside the version directory.

## Default Next-Step Standard

For each new version, maintain and update a claim-evidence matrix:

| Claim | Method component | Evidence artifact | Figure/Table | Boundary/Future Work |
|---|---|---|---|---|

Every major abstract/introduction claim must map to a row here or be downgraded.
