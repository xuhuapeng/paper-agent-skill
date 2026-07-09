# Citation And Literature Workflow

## Non-Negotiables

- Do not invent citations, venues, years, DOI values, arXiv IDs, or author lists.
- Prefer existing verified `.bib` entries when they already support the claim.
- Newly added references need a source: existing `.bib`, DOI/Crossref, arXiv, Semantic Scholar, OpenAlex, AMiner, official publisher page, or another explicit source.
- If verification is not possible in the turn, mark the entry or claim as `PLACEHOLDER_VERIFY` and keep the claim conservative.

## Literature Routing

Use the lightest route that can verify the claim.

| Need | Preferred route |
|---|---|
| Known title / DOI | Crossref, Semantic Scholar title match, arXiv, existing `.bib` |
| Find related work | Semantic Scholar / OpenAlex / AMiner / Elicit / PaperQA-style search |
| Citation chain | Semantic Scholar references/citations or AMiner paper relation |
| Venue/author metadata | Crossref + OpenAlex + publisher page cross-check |
| Systematic review | Elicit/PaperQA-style source table with evidence snippets |

Do not install heavy packages or use paid/API-key services by default. Treat them as optional routes and disclose tool use.

## Evidence Table

For serious literature changes, create or update an evidence table:

| Key | Title | Year | Venue/source | Verified by | Claim supported | Status |
|---|---|---:|---|---|---|---|

Statuses:

- `verified`: metadata and claim support were checked
- `local-bib-only`: entry exists locally but external metadata not checked this turn
- `placeholder`: needs human/API verification
- `remove`: citation does not support the claim or cannot be verified

## Manuscript Citation Audit

Before finishing:

1. Scan `\cite{}` keys used in `.tex`.
2. Scan keys defined in `.bib`.
3. Report missing keys and unused keys.
4. Report `PLACEHOLDER_VERIFY`, `[CITATION NEEDED]`, and suspicious future/unverified claims.
5. Ensure bibliography claims do not exceed evidence.

Use `scripts/audit_latex_refs.py` when available.