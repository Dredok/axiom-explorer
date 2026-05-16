# axiom-explorer

[![Methodology paper DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20184068.svg)](https://doi.org/10.5281/zenodo.20184068)
[![Conjecture paper DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20184660.svg)](https://doi.org/10.5281/zenodo.20184660)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An LLM-assisted experimental harness for systematic cross-search over
modern axiomatic seeds in mathematics, with explicit stop rules,
confidence-ladder labelling of every output, and a multi-round AI
peer-review loop before any human reviewer is approached.

This repository accompanies two preprints:

- **Paper A (methodology)** — *axiom-explorer: an LLM-assisted harness
  for cross-search over modern axiomatic seeds in mathematics, with one
  case study (condensed classifying anima envelope)*.
  DOI: [10.5281/zenodo.20184068](https://doi.org/10.5281/zenodo.20184068).
- **Paper B (case study)** — *A conjectural cardinality envelope for the
  condensed classifying anima of spectral $\infty$-topoi: a synthesis
  across geometric and analogical instances*.
  DOI: [10.5281/zenodo.20184660](https://doi.org/10.5281/zenodo.20184660).

Both are CC-BY-4.0 and open access on Zenodo.

## What this is

axiom-explorer takes a small set of *productive and recent* axiomatic
frameworks from distinct branches of mathematics, runs a structured
bibliometric and formal-state sweep over their pairwise combinations,
builds dossiers integrating literature, finite-case sanity checks
(Z3, SymPy) and where applicable Lean 4 axiomatic skeletons, and
filters surviving candidates against four explicit relevance tests.

The role of the large language model is bounded by four hard stop
rules (see Paper A §3.3) and the human author retains final approval
on every release, publication, and external communication.

## What this is not

- It is not a proof. The case-study output is a falsifiable
  conjecture registered for community feedback.
- It is not a claim that LLM-assisted workflows can replace
  expert mathematical review.
- It is not a comparative evaluation across LLMs or prompting
  strategies. It describes one configuration that ran end-to-end and
  produced a checkable, citable artefact.

## Repository layout

```
paper/
  methodology/   LaTeX source of Paper A (preprint.tex + references.bib)
  conjecture/    LaTeX source of Paper B (preprint.tex + references.bib)
docs/
  00-hypothesis.md         the original hypothesis the experiment tests
  01-methodology.md        the design of the workflow
  seeds/A{1..4}.md         per-seed cards for the case-study quadruple
  synthesis/CONJECTURE.md  the synthesised statement of the candidate
research/
  phase0-bibliometric/  arXiv/Scholar density map across the 6 binary combos
  phase1-formal-state/  Mathlib4 inventory and gaps
  phase2-binary-combos/ per-pair dossiers (A2xA3 and A1xA2 advanced)
  phase3-deep-dives/    full dossiers for surviving candidates
  phase4-final-report/  ranking, evidence, honest false-positives, meta
  phase5-pi-n-cond/     higher-pi forward question (K3 at n=2)
src/axiom_explorer/   Python implementation of the harness phases
data/phase0/raw/      raw arXiv query results (reproducible)
lean/                 Lean 4 axiomatic skeleton of Synthetic Stone Duality
tests/                pytest suite for the harness (51 tests)
notebooks/            exploratory notebooks (Jupyter)
```

## Running the harness locally

```bash
uv venv .venv
source .venv/bin/activate
uv sync --extra dev
pytest -q
axiom-explorer --help
```

To run a phase end-to-end:

```bash
python -m axiom_explorer.run_phase phase0
```

To build either preprint PDF locally (requires a TeX Live install):

```bash
cd paper/methodology
latexmk -pdf -interaction=nonstopmode preprint.tex
```

The Lean 4 skeleton builds with `lake build` from the `lean/`
directory, using the toolchain pinned in `lean/lean-toolchain`.

## Hypothesis (short form)

> Iterating deductively from modern productive axioms across multiple
> branches, with expert-curated relevance filtering on the output, has
> higher density of potentially-relevant findings per unit of search
> than iterating from classical axioms — because (i) the frontier is
> by definition less-explored, and (ii) modern axioms are pre-selected
> by the community for fertility.

Full statement: [`docs/00-hypothesis.md`](docs/00-hypothesis.md).

## Axiomatic seeds (case study)

| # | Framework                                | Branch                       |
|---|------------------------------------------|------------------------------|
| A1 | Univalence Axiom (HoTT)                 | Foundations                  |
| A2 | Condensed Mathematics (Clausen-Scholze) | Topology / Functional Analysis |
| A3 | Perfectoid Spaces (Scholze)             | Arithmetic Geometry          |
| A4 | Synthetic Ricci Curvature (LSV)         | Analysis / Metric Geometry   |

Detail on each seed in [`docs/seeds/`](docs/seeds/).

## Confidence ladder

Every claim that survives Phase 4 carries a confidence label:

- **L0** — verified mechanically.
- **L1** — strong: a standard, cited result.
- **L2** — plausible: argued, not directly verified.
- **L3** — speculative: a guess emerging from the cross-search.

The cardinality envelope candidate sits at **L2** for the upper bound
and **L3** for the saturation question.

## Honesty contract

- Every claimed novel candidate carries an **explicit confidence level**
  and a literature search trace.
- False positives are **reported, not silenced**.
- Re-discovery from a new route is treated as a valid result, not a
  failure.

## Stop rules

The harness pauses and reports to the human operator on any of:

1. **Significant finding** that passes all four relevance tests.
2. **Hard technical block** (required tool inaccessible, compute out of
   scope).
3. **Negative convergence** — all combinations exhausted with no
   surviving candidates.
4. **Irreversible decision** — any change of scope requires explicit
   approval.

## Citing this work

If you build on the methodology, please cite Paper A:

> Vera Gómez, Francisco Javier. *axiom-explorer: an LLM-assisted harness
> for cross-search over modern axiomatic seeds in mathematics, with one
> case study (condensed classifying anima envelope)*. Zenodo, 2026.
> [doi.org/10.5281/zenodo.20184068](https://doi.org/10.5281/zenodo.20184068)

If you engage with the conjecture, please cite Paper B:

> Vera Gómez, Francisco Javier. *A conjectural cardinality envelope for
> the condensed classifying anima of spectral $\infty$-topoi: a
> synthesis across geometric and analogical instances*. Zenodo, 2026.
> [doi.org/10.5281/zenodo.20184660](https://doi.org/10.5281/zenodo.20184660)

## License

All content in this repository is released under the
[Creative Commons Attribution 4.0 International License](LICENSE).

## Author

Francisco Javier Vera Gómez ·
[ORCID 0009-0001-3516-5871](https://orcid.org/0009-0001-3516-5871)
