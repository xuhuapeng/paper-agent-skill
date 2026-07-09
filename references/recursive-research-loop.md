# recursive-research-loop

A domain-agnostic recursive evidence-gathering workflow, inlined here so this skill
has no external dependency. Use it when a key judgment depends on several unverified
premises, instead of issuing one confident verdict.

## When to use (in this skill)

- Deciding whether a method / extension can move from Future Work into the method.
- Judging whether a contribution or experimental claim has adequate evidence.
- Auditing a batch of citations / BibTeX / dataset claims for truthfulness.

Do not use it for Mode A micro-edits (wording, a single caption).

## Core loop

```
RESEARCH-LOOP(question, depth=0):
  1. Plan       split the question into 2-5 sub-questions
  2. Execute    gather evidence per sub-question: local files/history first, public search as fallback
  3. Grade      tag each piece Confirmed / Inferred / Needs-verification
  4. Critique   look for four faults: gaps, over-inference, self-contradiction, fabrication risk
  5. Gate       if a key sub-question is still Needs-verification and depth < MAX_DEPTH
                   -> recurse only on that sub-question
                else stop
  6. Synthesize conclusion first, each tagged with its evidence grade, plus an open-items list
```

## Evidence grades (shared vocabulary)

- **Confirmed**: directly supported by a file line, history, an auditable artifact, or a reliable public source; the citation must trace to a specific location.
- **Inferred**: a reasonable inference from existing evidence but without direct proof; label it explicitly as inference.
- **Needs-verification**: key and unverified; needs the counterpart's confirmation, an official system, a private artifact, or a manual check.

## Hard stop conditions (anti-runaway)

1. **MAX_DEPTH = 2**: recurse at most two levels; a still-unverified sub-question at the cap is downgraded to "needs human/manual check," not chased further.
2. **MAX_SEARCHES**: cap external citation checks at <= 6 per round; on hitting it, mark unresolved citations `⚠️ unresolved` and stop — do not guess.
3. **Grades cannot be self-upgraded**: if the reviewer role finds Inferred/Needs-verification written as Confirmed, force it back down.
4. **Citations must be traceable**: every Confirmed must point to a specific file line or public source; if it cannot, it drops to Inferred.

Rules 3 and 4 exist because an agent under long-task/timeout pressure tends to "report done / report heard" without proof. The loop defends against that with forced downgrade rather than trust.

## Paper-domain specifics

- Default the sub-question split into three premises and gather evidence on each: **implemented** (is there runnable/reproducible code?), **experimental** (real evidence, or only proxy/synthetic?), **self-consistent** (do Figure 1 / abstract / intro / method agree?).
- Reuse this skill's existing machinery for the Critique step: the layered verification in `references/verification-layers.md`, the multi-reviewer simulation in `references/top-conference-review.md`, and the known failures in `evals/`.
- Strongest stop rule: a not-yet-implemented extension stays in future work unless all three premises hold; if any fails, reverse direction to "why it cannot go in yet + which three kinds of evidence would be needed to promote it."

## Output (Synthesize step)

Conclusion first + each conclusion tagged Confirmed / Inferred / Needs-verification + an open-items list. For Mode B/C, still produce an Iteration Review per `references/iteration-review-template.md`.
