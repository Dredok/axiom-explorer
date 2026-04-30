# ADR 0001 — Workspace scaffolding

- **Date**: 2026-05-01
- **Status**: Accepted

## Context

The user requested an autonomous experiment to test whether iterating
deductively over modern productive axioms across distinct branches yields
a higher density of relevant findings than iterating from classical axioms.
The harness needs to persist artifacts, support reproducibility, and
integrate with the existing GitLab CI ecosystem at `gitlab.loneorc.com`.

## Decision

Create a new GitLab project at `research/axiom-explorer` (private), cloned
locally to `/mnt/fastpool/research/axiom-explorer/`, scaffolded as a
Python `uv` + `hatchling` package mirroring the conventions of
`research/pnp-sat-lab` and `vera-studio/vera-obs`:

- `.gitlab-ci.yml` includes `vera-studio/ci-templates@release/1.13` for
  `common.yml`, `python-jobs.yml`, `code-review.yml`.
- Stages: `review`, `lint`, `test`, `research`. The `research` stage is a
  manual job parameterized by `RESEARCH_PHASE` so that long phases can be
  reproduced in CI with persisted artifacts.
- Layout separates source (`src/axiom_explorer/`), per-phase outputs
  (`research/phaseN-<name>/`), raw data (`data/phaseN/`), notebooks
  (`notebooks/`) and ephemeral artifacts (`artifacts/`, gitignored).
- Lean 4 deferred to first formalizable candidate.
- Auto-merge on green CI permitted for this single-dev research repo.

## Consequences

- Consistent with the rest of the GitLab ecosystem; PR-Agent and review
  flow available out of the box.
- Reproducibility: every external query persists raw response + query
  signature + timestamp.
- Per-phase output location is stable, so the final report can cite
  artifacts by path.
- Lean deferral keeps the initial setup light; will be revisited at Phase 2.
