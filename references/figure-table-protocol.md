# Figure And Table Protocol

## Figure Brief

Start every important figure/table with:

| Field | Question |
|---|---|
| Reviewer question | What objection or confusion does this artifact answer? |
| One-sentence takeaway | What should the reviewer remember? |
| Abstraction level | model, system, training, serving, result, monitoring, or limitation |
| Required entities | which modules/signals must appear |
| Excluded details | what is intentionally hidden |
| Provenance | source image/script/data/table path |
| Text anchor | where the paper cites it |

## Artifact Types

- Figure 1: core contribution and paper story.
- Model diagram: computation, losses, gradients, detach paths.
- System diagram: offline/online/deployment/release boundaries.
- Result plot: evidence for a claim or failure mode.
- Table: exact comparison, ablation, or claim-evidence mapping.
- Case figure: behavior hidden by aggregate metrics.

## Visual Grammar

- solid arrows: forward data flow
- dashed arrows: auxiliary signal or supervision
- dotted arrows: detach/stop-gradient path
- shaded bands: offline, training, serving, monitoring, future-work
- explicit tags: implemented, proxy, proposed, future work

Do not mix abstraction levels unless separated by panels or bands.

## Example: architecture-figure required entities

For a system/architecture Figure 1, list every entity the figure must show so the
figure, abstract, and method agree. Below is a worked example for a
generative-recommendation paper — replace it with your own component list:

- offline tokenizer build (e.g. residual-quantized k-means)
- item / user representations
- shared sequence encoder
- multi-task routing (e.g. MMoE)
- autoregressive ID decoder
- exposure/reachability head
- utility heads (CTR/CVR/CTCVR)
- detached exposure residual
- full-space conversion objective (e.g. ESMM-style)
- gradient balancing if claimed (e.g. GradNorm)
- dynamic top-K serving
- release monitoring gates

## LaTeX Figure QA

Before finalizing:

1. figure files exist and are non-empty
2. `\includegraphics` paths match exported assets
3. cropped raster figures prefer PNG in `acmart` unless vector PDF is known clean
4. every figure has caption, label, and `\Description{}` when using `acmart`
5. labels are referenced in text
6. rendered PDF pages are visually checked for high-risk figures
7. no stale version labels such as `fig:v5_` in v6 manuscripts

Use `scripts/audit_figures.py` when available.

## Tables

Prefer compact tables that expose decision logic:

- method family
- deployability
- tokenizer requirement
- objective/loss
- serving cost
- bias/exposure handling
- evidence status

Avoid huge inventory tables that do not support a claim.