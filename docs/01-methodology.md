# Methodology

## Roles

- **Harness** (Python package `axiom_explorer`): mechanical search, query
  execution, data persistence, light analysis, statistics.
- **Expert curator** (LLM agent + human operator): semantic filtering,
  relevance judgement, interpretation of results, decision to escalate or
  drop a candidate.
- **External tools**: arXiv API, Mathlib4 source, OEIS, LMFDB, ATPs (when
  needed), Sage/Macaulay2/Singular (when needed), Lean 4 (deferred).

The harness is *not* an oracle. It is a focused information-gathering and
bookkeeping tool. All judgement calls are logged with rationale.

## Phases

### Phase 0 — Bibliometric mapping

Goal: produce a heat map of the 6 binary combinations of the 4 seeds, by
density of existing literature, to identify (a) saturated combinations
(novelty unlikely) and (b) sparse combinations (high novelty potential, but
also possibly a sign of inherent incompatibility).

Tools: arXiv API (Atom feed), web search, manual cross-check on
MathOverflow / nLab for borderline cases.

Output: `research/phase0-bibliometric/REPORT.md` plus raw search dumps in
`data/phase0/*.json`.

### Phase 1 — Formal-state inventory in Mathlib4

Goal: for each seed, identify what is already formalized in Mathlib4 and
adjacent projects (Liquid Tensor Experiment, perfectoid-spaces, etc.).
Surface formalization gaps that double as potential targets.

Tools: shallow clone of Mathlib4, ripgrep over the source tree.

Output: `research/phase1-formal-state/REPORT.md`.

### Phase 2 — Binary combinations

Goal: for each surviving binary combination from Phase 0, identify the
**bridging functor or construction** that connects the two frameworks, and
attempt to produce candidate statements that genuinely require both.

Tools: literature follow-up, small-case computation in Python/Sage,
ATP-assisted lemma checking when applicable.

Output: per combination, `research/phase2-binary-combos/<AxAy>/REPORT.md`.

### Phase 3 — Deep dives

Goal: for each candidate that survives Phase 2 filtering, build a full
dossier: precise statement, evidence for and against, semantic search of
exact and near-exact statements in literature, partial Lean formalization
if feasible.

Output: `research/phase3-deep-dives/<candidate-id>/dossier.md`.

### Phase 4 — Final filtering and report

Apply the four relevance tests:

1. **Novelty test**: not in known literature up to harness cutoff.
2. **Inter-branch connectivity**: touches at least 2 of the 4 seed branches.
3. **Open-problem tangency**: rigorously connected to a recognized open
   conjecture or to a structural question in an active program.
4. **Non-triviality**: the proof or statement genuinely requires the
   combination; reducible cases are demoted.

Output: `research/phase4-final-report/REPORT.md` with ranking, dossiers,
honest false-positives section, and meta-analysis of which tools and
combinations were most productive.

## Branching, commits, MRs

- One branch per phase: `feat/phase0-bibliometric-map`,
  `feat/phase1-formal-state`, etc.
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `data:`.
- Each phase produces an MR. CI must be green to merge.
- This being a single-developer research repo, auto-merge is allowed once
  the phase report is complete and CI passes.

## Persistence and reproducibility

- All external queries log timestamp + exact query in `data/<phase>/queries.jsonl`.
- Raw API responses stored as JSON in `data/<phase>/raw/`.
- Derived analyses re-runnable from raw data via scripts in
  `src/axiom_explorer/`.
- Confidence levels for every claim follow a 4-step ladder:
  - **L0 — Verified**: directly checked in source or formal system.
  - **L1 — Strong**: standard result in the cited literature.
  - **L2 — Plausible**: argued by the harness, not directly verified.
  - **L3 — Speculative**: emerged from combination, not yet checked.

L3 claims may be reported but never as conclusions.

## Stop rules (recap)

See README. The harness escalates to the human operator on:
finding, hard block, negative convergence, or scope-changing decision.
