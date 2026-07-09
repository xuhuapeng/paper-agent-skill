# Verification Layers (Why Audits Missed Defects, and the Layered Fix)

Load this when finishing any non-trivial paper edit, before declaring the
manuscript "clean". It exists because structural audits passed while real
defects shipped.

## Postmortem: why earlier reviews missed real defects

The v6 pass ran four structural audits (refs, bib metadata, figures, claim
language), all green, yet three defect classes survived:

1. **Visible column overlap (overfull `\hbox`).** The abstract contained the
   slash compound `exposure/reachability`, an unbreakable token that spilled
   33pt out of the left column and overlapped the right column on page 1.
   *Root cause:* every structural audit reads the `.tex`/`.bib` source. None of
   them looks at the rendered PDF, so a layout defect is invisible to them. A
   clean compile is **not** a clean layout — `tectonic` emits overfull boxes as
   non-fatal warnings and still produces a PDF.

2. **Duplicate bibliography entries.** Four pairs (`jegou2011pq`/`jegou2011`,
   `ge2013opq`/`ge2013`, `babenko2014aq`/`babenko2014`, `zhang2014cq`/`zhang2014`)
   described the same paper under different keys. *Root cause:* the refs audit
   only computed `used − defined` and `defined − used`. The duplicate keys with
   distinct names were simply reported inside a large `UNUSED_BIB_KEYS` list and
   were not flagged as a duplicate defect class, so they read as "harmless
   unused entries" instead of "redundant references to delete".

3. **Table-column overclaim.** A results column was labelled `GMV`, implying a
   real business metric, when the number was a synthetic proxy. *Root cause:* the
   claim-language audit scans prose for absolute-claim words; it never inspects
   table header semantics, so an overclaiming column name passes silently.

General lesson: **source-level structural checks cannot certify rendered output
or semantic intent.** They prove the source is internally consistent, not that
the artifact a reviewer sees is correct. Treat every all-green audit run as
"necessary, not sufficient".

## The layered verification model

Run the layers in order. A later layer may fail even when every earlier layer
passes; do not skip the visual and semantic layers.

| Layer | Question it answers | How | Failure it catches |
|---|---|---|---|
| L1 Source consistency | Do source artifacts cross-reference correctly? | `audit_latex_refs.py`, `audit_figures.py` | missing/unused/duplicate cites, broken labels, missing `\Description` |
| L2 Metadata honesty | Is every reference real and complete? | `audit_bib_metadata.py` + external verification of new keys | hallucinated/incomplete BibTeX |
| L3 Claim language | Does prose overclaim beyond evidence? | `audit_claim_language.py` + manual claim-evidence matrix | unsupported production/SOTA/causal claims |
| L4 Build | Does it compile? | `tectonic main.tex` | hard LaTeX errors |
| L5 **Layout (visual)** | Does the *rendered* page look correct? | `audit_layout.py` to list visible overfull boxes, then **render the flagged pages to images and inspect** | column overlap, runaway tokens, clipped figures/tables |
| L6 **Semantic intent** | Do labels, headers, and captions mean what they claim? | manual read of every table header, axis label, and figure caption against the evidence boundary | proxy-as-real metric names, mislabeled axes, caption drift |

### L5 procedure (the layer that was missing)

1. `python3 scripts/audit_layout.py <paper_dir> --threshold 12` to list overfull
   boxes large enough to be visible.
2. For each flagged source line, render the corresponding page(s) to PNG (e.g.
   PyMuPDF `fitz.Matrix(2,2)`) and look for text crossing a column boundary or
   overrunning the margin.
3. A flagged box is only a real defect if it is **visible** — justified text and
   microtype often absorb a >12pt warning with no overlap. The script proposes
   candidates; the human/visual pass is the verdict.
4. Fix real overlaps at the source token: replace unbreakable slash compounds
   (`a/b`) with `a and b`, add hyphenation points, or reword. Recompile and
   re-render to confirm.

### L6 checklist

- Every table column name is either a real measured quantity or explicitly
  marked as a proxy (e.g. `GMV proxy`, with a caption caveat).
- Absolute metric magnitudes that look surprising are explained in the caption.
- Figure captions describe what the figure actually shows in the current version.

## Definition of done for a paper edit

A paper edit is "clean" only when L1–L4 pass **and** L5 was rendered-and-inspected
**and** L6 was manually walked. If any layer is skipped, say so explicitly in the
work report rather than implying full verification.
