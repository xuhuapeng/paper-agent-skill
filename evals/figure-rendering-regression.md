# Eval: Figure Rendering Regression

## Historical Failure

In one paper version, Figures 2/3/4 were cropped correctly as PNG/PDF, but the manuscript macro preferred same-stem PDF files. The raster-to-PDF wrappers rendered poorly inside `acmart` floats, causing the final PDF to show captions while hiding figure bodies.

## Expected Agent Behavior

- Inspect source PNG/PDF assets, not only LaTeX references.
- Prefer PNG for raster crops unless the PDF is known to be a clean vector or correctly boxed PDF.
- Run or recommend `scripts/audit_figures.py`.
- Compile the paper and visually inspect rendered PDF pages for high-risk figures.
- Document the macro behavior in the paper version README/report.

## Failure Signal

The agent says "all figures are inserted" based only on grep or `pdftotext`, without checking visual rendering.