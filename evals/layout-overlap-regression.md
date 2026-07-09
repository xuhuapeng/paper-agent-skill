# Regression: rendered-layout overlap not caught by source audits

## Symptom

In one paper version, the abstract on page 1 visibly overlapped the right column: the
word `reachability` from the slash compound `exposure/reachability` ran past the
left column boundary and printed on top of the right column text. All four
structural audits (refs, bib metadata, figures, claim language) were green and
`tectonic` produced a PDF without errors.

## Root cause

- Structural audits only read `.tex`/`.bib` source; none inspects the rendered
  PDF, so a layout defect is invisible to them.
- `tectonic` reports overfull `\hbox` as a non-fatal warning and still emits a
  PDF, so "compiles" did not imply "lays out correctly".
- The offending token was an unbreakable slash compound (`a/b`) that TeX could
  not hyphenate, forcing a 33pt overflow.

## Fix applied

- Reworded `supervised exposure/reachability prediction` →
  `supervised exposure and reachability prediction` so the line can break.
- Recompiled and re-rendered page 1 to confirm the overlap was gone.

## Prevention (now encoded in the skill)

- Added `scripts/audit_layout.py`: compiles and lists overfull boxes >= a visible
  threshold, then instructs the reviewer to render-and-inspect the flagged pages.
- Added `references/verification-layers.md` defining L5 (visual layout) and L6
  (semantic intent of headers/labels/captions) as mandatory layers beyond source
  audits.
- Rule of thumb: replace unbreakable `a/b` slash compounds in abstracts/titles
  with `a and b`, and never declare layout clean from a successful compile alone —
  render the pages flagged by the layout audit.

## Related defects found in the same pass

- Four duplicate bib entries (`*pq/opq/aq/cq`) hid inside `UNUSED_BIB_KEYS`;
  `audit_latex_refs.py` now emits `DUPLICATE_BIB_TITLES`.
- A results column labelled `GMV` was a synthetic proxy; renamed to `GMV proxy`
  with a magnitude caveat in the caption (L6 semantic-intent check).
