# Preprint checklist — axiom-explorer v1

This checklist defines the minimum bar for releasing the synthesis preprint
on Zenodo.

Patterned on the equivalent checklist of the V.E.R.A. preprint
(`research/vera-paper`, gitlab.loneorc.com).

## Scientific framing

- [ ] Title and abstract describe the work as a **synthesis preprint**, not as
      a primary research result.
- [ ] The paper does **not** claim to have proved the cardinality envelope.
      It is presented as a falsifiable **conjecture** with three corroboration
      angles.
- [ ] The novelty claim is narrow and explicit: "the uniform formulation
      across the unification, not the individual statements".
- [ ] The unification of geometric and model-theoretic sides is credited to
      Haine 2026 and forthcoming Haine-Damaj-Zhang, **not** to this preprint.
- [ ] Author position declared explicitly (software/methodology background,
      not frontier-mathematics expert).
- [ ] LLM-assisted production method declared explicitly with the repo URL.
- [ ] Confidence level labelled per claim (L0/L1/L2/L3).

## Required validation

Before tagging or submitting, run from the repository root:

```bash
uv sync --extra dev
uv run ruff check .
uv run pytest -q
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error preprint.tex
cd ..
python3 scripts/build_publication_bundle.py --allow-dirty
```

Expected outputs:

```
paper/preprint.pdf
dist/publication/axiom-explorer-v1-preprint-zenodo.zip
dist/publication/axiom-explorer-v1-preprint-arxiv-source.zip
```

## Mandatory placeholder replacements before publishing

The following fields contain `XXXX-XXXX-XXXX-XXXX` or other placeholders
that **must be filled in** before the user clicks "Publish" on Zenodo:

- [ ] `paper/preprint.tex` — author ORCID in the `\affil` block
- [ ] `.zenodo.json` — `creators[0].orcid`
- [ ] `CITATION.cff` — `authors[0].orcid` and `preferred-citation.authors[0].orcid`

A grep for `XXXX-XXXX-XXXX-XXXX` in the repo root returns the exact lines.

## Pre-publication review

- [ ] Read the full PDF top to bottom; flag any over-claim that crept in.
- [ ] Verify every `\cite{...}` resolves to the right paper.
- [ ] Verify the conjecture is stated identically in:
      - `paper/preprint.tex` (Conjecture 1)
      - `docs/synthesis/CONJECTURE.md`
      - `.zenodo.json` description
- [ ] Verify the seven attestations table (Section 4) is consistent with the
      bibliography.
- [ ] Verify the falsifiability section is sharp enough that an expert
      could falsify with a single counterexample.

## Recommended first public target — Zenodo

The user creates a new Zenodo upload manually using the `.zenodo.json`
metadata. The bundle ZIP under `dist/publication/` is uploaded as the
software/data attachment. The PDF is uploaded as the primary publication.

DOI is reserved by Zenodo at the "Save" stage and the user reviews every
field one final time before clicking "Publish". **The orchestrator does NOT
publish on the user's behalf** — this is an explicit stop rule.

## After publication

- [ ] Update `.zenodo.json` with the assigned DOI.
- [ ] Update `CITATION.cff` with the assigned DOI.
- [ ] Issue a release commit `release: v1-preprint` and a matching git tag.
- [ ] Send the courtesy email to Peter J. Haine (template:
      `.agent/EMAIL_DRAFT_HAINE.md`, kept local only) with the DOI included.
- [ ] Optional: notify Cherubini-Coquand-Geerligs-Moeneclaey for the Lean
      skeleton link, Bergfalk-Lambie-Hanson for the set-theoretic angle.
