# paper-agent-skill

**English** · [中文](README.zh-CN.md)

> A versioned, multi-layer verification workflow for iterating on serious LaTeX research papers with an AI coding agent — so that "the source compiles" never gets mistaken for "the paper is correct."

**中文简介（TL;DR）**：这是一套把「论文当成带版本的可审计系统」来迭代的 agent skill。它不只帮你润色文字，而是先锁定 claim–evidence 契约，再用 5 个确定性审计脚本 + 6 层校验（源码一致性 → 元数据诚实 → 过度声明 → 编译 → 版面视觉 → 语义意图）把常见的「结构审计全绿、PDF 却仍有毛病」这类缺陷抓出来。**已去身份、通用化；用前按下方 Configuration 把占位路径换成你自己的项目即可。**

---

## What this is

`paper-agent-skill` is an [Agent Skill](https://www.anthropic.com/news/skills) (a folder of instructions + scripts + reference docs that an AI agent loads on demand). It encodes a discipline for **serious, multi-round research-paper iteration**, as opposed to one-shot "polish my English."

The central belief: a research paper is not prose to be smoothed, it is a **claim–evidence contract**. Every claim in the abstract and introduction must map to a real method component, a real experiment artifact, and a figure/table — or be downgraded. The skill's job is to keep the agent honest about that mapping, and to catch the defects that a naive "it compiled, ship it" pass misses.

## Why it exists (the problem it solves)

When you iterate on a paper with an LLM over many rounds, three failure modes recur:

1. **Performed rigor.** The model writes every claim airtight and every sentence smooth, which quietly inflates "might help" into "significantly improves" and "proxy metric" into "business metric."
2. **Source-clean but artifact-broken.** Citation/label/figure audits all pass, `tectonic` produces a PDF with no errors — and yet page 1 has a line spilling out of its column onto neighbouring text, or a table header silently renames a synthetic proxy as a real metric. Structural checks read the `.tex`; they never look at the rendered page.
3. **Memory drift.** Over many editing rounds the model reintroduces something you cut three sections ago, or contradicts a definition it wrote earlier. Attention favors recent context; long-horizon consistency is on you.

This skill turns the parts that *can* be mechanized into deterministic checks, and names the parts that still require human judgment so they are not silently skipped.

## Architecture

Thin router + thick references + deterministic scripts + regression memory:

```
paper-agent-skill/
  SKILL.md                     # thin router: triggers, when-to-load, non-negotiables, modes, workflow
  references/                  # loaded on demand, one topic each
    manuscript-workflow.md       # version recovery, rewrite modes, structural workflow
    project-baseline.md          # per-project baseline template + common LaTeX gotchas
    citation-literature-workflow.md
    figure-table-protocol.md     # figure/table design + LaTeX figure QA
    verification-layers.md       # the L1–L6 layered-verification model
    top-conference-review.md     # top-venue checklist + multi-reviewer simulation
    iteration-review-template.md # final review report shape
    recursive-research-loop.md   # self-contained recursive evidence-gathering loop
  scripts/                     # stdlib-only Python, advisory (never a hard CI gate)
    audit_latex_refs.py          # missing/unused/duplicate cites, placeholders, stale version labels
    audit_bib_metadata.py        # BibTeX entry count + missing DOI/arXiv/URL metadata
    audit_figures.py             # figure existence, caption, label, \Description, referenced labels
    audit_claim_language.py      # scans prose for over-claim / absolute / causal / production wording
    audit_layout.py              # compiles + reports visible overfull \hbox, tells you which pages to render
  evals/                       # regression memory: known failure modes with real cases
    citation-hallucination-case.md
    figure-rendering-regression.md
    overclaiming-review-case.md
    layout-overlap-regression.md
```

### The verification layers (the heart of the skill)

A clean compile and green source audits are **necessary but not sufficient**. Run in order; a later layer can fail even when every earlier one passes:

| Layer | Question | How | Catches |
|---|---|---|---|
| L1 Source consistency | Do source artifacts cross-reference correctly? | `audit_latex_refs.py`, `audit_figures.py` | missing/unused/duplicate cites, broken labels, missing `\Description` |
| L2 Metadata honesty | Is every reference real and complete? | `audit_bib_metadata.py` + external verification | hallucinated / incomplete BibTeX |
| L3 Claim language | Does prose over-claim beyond evidence? | `audit_claim_language.py` + claim–evidence matrix | unsupported SOTA / causal / production claims |
| L4 Build | Does it compile? | `tectonic main.tex` | hard LaTeX errors |
| **L5 Layout (visual)** | Does the *rendered page* look right? | `audit_layout.py` → then render flagged pages to images and look | column overlap, runaway tokens, clipped figures/tables |
| **L6 Semantic intent** | Do headers/labels/captions mean what they claim? | manual read against the evidence boundary | proxy-as-real metric names, mislabeled axes, caption drift |

L5 and L6 are the layers that pure source audits cannot cover, and are exactly where "0 audit errors" papers still ship visible defects.

### Operating modes

- **Mode A — Local patch:** small wording/citation/equation/caption/table change. Patch, targeted-validate, report residual risk.
- **Mode B — Structural rewrite:** positioning/novelty/method/experiment/figure-system change. Lock the one-sentence contribution, Figure 1 reviewer question, claim–evidence matrix, evidence boundary; rewrite; compile; audit; produce an Iteration Review.
- **Mode C — Algorithm/architecture change:** tokenizer/model/loss/serving/baseline/ablation change. Classify each claim as implemented / proxy / proposed / future work and align paper↔code↔runbook or downgrade the claim.
- **Mode D — Review/strategy memo:** critique without source edits; lead with findings and prioritized repairs.

## Who this is for (applicability)

Good fit if you:

- Write **LaTeX** papers (built here with [`tectonic`](https://tectonic-typesetting.github.io/); `acmart` is the tested class) and iterate over many rounds.
- Work with an AI agent that can read files, run shell commands, and render PDFs.
- Care about **industry-track / systems-paper rigor** (RecSys / CIKM / WWW / KDD style), where claim honesty, reproducibility boundaries, and figure/table correctness matter more than literary polish.
- Want the boundary between *implemented*, *proxy experiment*, *proposed*, and *future work* enforced rather than blurred.

Weaker fit if you:

- Write in Word/Google Docs (the layout + audit scripts assume LaTeX source).
- Want a one-click "humanize / polish" button — this skill deliberately refuses shallow polishing before the claim/evidence chain is fixed.
- Need a hard CI gate — the scripts are **advisory** by design (they print findings and exit 0), because most warnings need human triage.

## Requirements

- **Python 3** (scripts are standard-library only, no `pip install`).
- **tectonic** (or another LaTeX engine) for L4/L5 build + overfull detection.
- A PDF rasterizer for L5 render-and-inspect: [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`), `pdftoppm`, or ImageMagick.
- An AI agent host that supports the Agent Skills format (the skill is host-agnostic Markdown + Python; it does not require any specific vendor).

## Quickstart

```bash
# run the deterministic audits against a paper version directory
python3 scripts/audit_latex_refs.py    /path/to/paper_dir
python3 scripts/audit_bib_metadata.py  /path/to/paper_dir
python3 scripts/audit_figures.py       /path/to/paper_dir
python3 scripts/audit_claim_language.py /path/to/paper_dir
python3 scripts/audit_layout.py        /path/to/paper_dir --threshold 12

# then: compile, and RENDER the pages flagged by audit_layout to images and look at them (L5),
# and read every table header / axis label / caption against your evidence boundary (L6).
```

The scripts assume a paper directory containing `main.tex` (with `\documentclass`), section `.tex` files, and a `.bib` file. `audit_layout.py` calls `tectonic` if present, otherwise parses an existing `.log`.

## Limitations & known problems

Honest list — read before trusting this:

1. **Advisory, not proof.** The scripts catch an *objectively checkable subset*. A clean run means "no mechanical red flags," not "the paper is correct." L5/L6 still require a human/agent to actually look at rendered pages and read captions.
2. **Regex-level checks.** Citation/label/claim detection is pattern-based. It can miss creatively-formatted `\cite`s, unusual float setups, or over-claims phrased outside the word list; and it can false-positive (e.g. a legitimately-repeated technical term). Treat every hit as "confirm," not "delete."
3. **Toolchain assumptions.** `acmart` + `tectonic` are the tested path. Other classes/engines may need tweaks. `audit_layout.py`'s overfull threshold (12pt) is a heuristic; small overfulls are often invisible.
4. **Placeholders, not autodetection.** Paths in `SKILL.md` and `references/project-baseline.md` are `<workspace>` / `<paper-root>` placeholders you fill in; the skill does not auto-discover your paper layout.
5. **The example domain is recommendation-systems.** The worked examples (tokenizer / Semantic-ID / utility heads) are illustrative, not a constraint — swap in your own architecture. The methodology is domain-agnostic; the samples are not.
6. **No packaged tests.** This is a working extraction, not a hardened library. The scripts are stdlib-only and self-checking, but there is no test suite yet — add smoke tests before treating it as a dependency.

## Configuration (set these for your project)

The skill ships de-identified and generic; point it at your own paper before use:

- In `SKILL.md` → *Quick Target Defaults*, replace `<workspace>` / `<paper-root>` / `<reports-dir>` with your real directories.
- Copy `references/project-baseline.md` and fill in your paper's canonical state, positioning, and evidence boundary.
- Set your *Default Evidence Stance* in `SKILL.md` (what the paper is/isn't, which parts are validated vs. proposed).
- Optional: add your not-yet-implemented extension names to `PROJECT_EXTENSION_TERMS` in `scripts/audit_claim_language.py` to flag them if claimed as done.
- Adjust `audit_layout.py --threshold` if your class/margins differ from `acmart`.

## License

MIT — see [LICENSE](LICENSE).

## Credits

Extracted from a personal, long-running paper-iteration skill. The layered-verification idea grew out of a real incident where every source audit passed but the rendered PDF still overlapped columns — see `evals/layout-overlap-regression.md`.
