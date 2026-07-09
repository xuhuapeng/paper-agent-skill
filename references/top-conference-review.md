# Top-Conference Review Reference

## Readiness Checklist

A serious paper revision is not complete until these line up:

1. Specific, defensible one-sentence contribution.
2. Figure 1 answers the main reviewer question.
3. Abstract covers context, gap, method, evidence, and implication.
4. Introduction states problem, gap, method idea, contributions, and proof path.
5. Problem formulation motivates each method component.
6. Method is reimplementable at the right abstraction level.
7. Experiments tie each metric/ablation to a claim.
8. Related work covers closest foundations and recent systems without selective citation.
9. Limitations are honest but do not destroy the central contribution.
10. Reproducibility, ethics, AI-use, and venue-specific requirements are handled when venue is known.

## Multi-Reviewer Gate

For serious reviews, synthesize five roles:

| Role | What to attack |
|---|---|
| Editor / relevance | Why should this paper exist and who cares? |
| Methodology / reproducibility | Can the method and results be reproduced? |
| Domain / prior art | Is the novelty real against closest work? |
| Systems / deployment | Are serving, monitoring, scaling, and failure modes credible? |
| Devil's advocate | Is this pseudo-innovation, overclaiming, or selective citation? |

A critical devil's-advocate issue blocks any ready-to-submit judgment until fixed or explicitly bounded with evidence.

## Anti-Shallow Rule

Do not make weak claims smoother. Fix the claim scope, evidence, and argument chain first.

## Venue Profiles To Consider

- RecSys / CIKM / WWW industry track: credible system boundary, production/deployment relevance, strong ablations, honest limitations.
- NeurIPS / ICML: clearer algorithmic novelty, theoretical or broad empirical evidence, rigorous baselines, reproducibility checklist.
- arXiv technical report: acceptable for architecture/evidence boundary, but must not sound like accepted production proof.

When venue is unknown, default to RecSys/CIKM/WWW industry-track standards.