# axiom-explorer

Autonomous experimental harness for deductive exploration over **modern axiomatic
seeds** in mathematics, with tooling-assisted relevance filtering.

## What this is

A research lab that takes a small set of *productive and recent* axiomatic
frameworks from distinct branches of mathematics, systematically explores their
binary, ternary and quaternary combinations, and uses real tooling
(arXiv/MathOverflow search, Mathlib4 introspection, Sage/SymPy/NumPy compute,
ATPs and theorem provers when justified) to surface candidate theorems or
inter-branch connections that may be **(a) novel, (b) tangent to known open
problems, or (c) shorter proofs of classical results from a new vantage point**.

Originated from a conversation about whether such a pipeline could systematically
shorten the distance to new mathematics by seeding the search at the *frontier*
rather than at classical foundations.

## Hypothesis (short form)

> Iterating deductively from modern productive axioms across multiple branches,
> with expert-curated relevance filtering on the output, has higher density of
> potentially-relevant findings per unit of search than iterating from classical
> axioms — because (i) the frontier is by definition less-explored, and (ii)
> modern axioms are pre-selected by the community for fertility.

Full hypothesis and methodology in [docs/00-hypothesis.md](docs/00-hypothesis.md)
and [docs/01-methodology.md](docs/01-methodology.md).

## Axiomatic seeds (current run)

| # | Framework                                | Branch                       |
|---|------------------------------------------|------------------------------|
| A1 | Univalence Axiom (HoTT)                 | Foundations                  |
| A2 | Condensed Mathematics (Clausen-Scholze) | Topology / Functional Analysis |
| A3 | Perfectoid Spaces (Scholze)             | Arithmetic Geometry          |
| A4 | Synthetic Ricci Curvature (LSV)         | Analysis / Metric Geometry   |

One short markdown per seed in [docs/seeds/](docs/seeds/).

## Repository layout

```
docs/                      # hypothesis, methodology, seed sheets, ADRs
research/                  # outputs by phase (markdown reports + data)
  phase0-bibliometric/     # arXiv/Scholar density map across the 6 binary combos
  phase1-formal-state/     # Mathlib4 inventory and gaps
  phase2-binary-combos/    # one subdir per combination (A1xA2, A1xA3, ...)
  phase3-deep-dives/       # full dossiers for surviving candidates
  phase4-final-report/     # ranking, evidence, honest false-positives, meta
src/axiom_explorer/        # Python package: search clients, compute, relevance
data/                      # raw search outputs (JSON), reproducible
notebooks/                 # exploratory Jupyter (Sage when needed)
tests/                     # smoke tests for clients and core logic
```

## Running locally

```bash
uv venv .venv && source .venv/bin/activate
uv pip install -e ".[all]"
pytest -q
axiom-explorer --help
```

## Running a phase

```bash
# Local
python -m axiom_explorer.run_phase phase0

# In CI (manual job, see .gitlab-ci.yml)
# Trigger pipeline with variable: RESEARCH_PHASE=phase0
```

## Reports

Every phase produces a `REPORT.md` under `research/<phase>/`. The final
synthesis lives in `research/phase4-final-report/REPORT.md`.

## Stop rules

The harness stops and reports to the human operator on any of:

1. **Significant finding**: a candidate that passes all four relevance tests.
2. **Hard technical block**: required tool inaccessible or compute out of scope.
3. **Negative convergence**: all combinations exhausted with no surviving
   candidates — also a result.
4. **Irreversible decision**: any change of scope (replace a seed, add a new
   branch) requires explicit approval.

## Honesty contract

- Every claimed novel candidate carries an **explicit confidence level** and
  **literature search trace**.
- False positives are **reported, not silenced**.
- "Re-discovery from a new route" is treated as a valid result, not a failure.

## Status

See [.agent/checkpoint.md](.agent/checkpoint.md) (gitignored, local state).
Public progress: GitLab issues tagged by phase.

---

## Current state (autonomous run completed)

After a full autonomous Phase 0 -> Phase 5 sweep:

- **Top candidate**: C-A2A3-2 cardinality envelope `|π_1^{cond}(X_k)| <= 2^|k|`, with
  three independent corroboration angles (geometric, model-theoretic, set-theoretic).
  L2-strong; falsifiable; structural argument written. See
  [research/phase4-final-report/REPORT.md](research/phase4-final-report/REPORT.md).
- **L0 verified deliverable**: Lean 4 axiomatic skeleton of Synthetic Stone Duality
  in `lean/AxiomExplorer/SyntheticStoneDuality.lean`. Builds clean.
- **Negative control**: A3 x A4 (Perfectoid x Synthetic Ricci) confirmed as
  bibliometrically and structurally sparse.
- **Methodology delta**: Q5 author-topic search added to the bibliometric harness
  (Phase 0 v4); now catches Cherubini-Coquand and Mann/Haine/Scholze cross-area
  work autonomously.
- **Forward question (Phase 5)**: does the envelope extend to higher π_n^{cond},
  n >= 2? Most informative test case identified: K3 surface at n=2.

Hypothesis qualitatively corroborated: cross-search across modern axiomatic
seeds did surface fresh cross-branch unification (announced in 2024-2026 papers).
The strongest output is a conjecture, not a theorem.

