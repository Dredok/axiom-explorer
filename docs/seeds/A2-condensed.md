# A2 — Condensed Mathematics

- **Branch**: Topology / Functional Analysis
- **Origin**: Clausen-Scholze, 2019 onward (lectures at Bonn).
- **Statement (informal)**: Replace the category of topological spaces with
  the category of *condensed sets* — sheaves on the site of profinite sets.
  This site is "well-behaved" enough to make functional analysis a clean
  homological theory.
- **Why productive**:
  - Resolves long-standing technical issues in functional analysis where
    standard topological vector space theory fails to be abelian.
  - **Solid** and **liquid** module theories give rigorous frameworks for
    p-adic and real/complex functional analysis respectively.
  - Liquid Tensor Experiment (LTE) formalized a key liquid theorem in Lean,
    establishing reach into real analysis.
- **Active programs**:
  - Condensed K-theory, condensed homotopy theory, condensed Hodge theory.
- **Formalization status**:
  - Mathlib4 has `Mathlib.Condensed.*`. Liquid Tensor Experiment is a
    separate, completed Lean project.
- **Known tensions / non-trivial bits**:
  - Set-theoretic size issues — needs careful handling of cutoff cardinals
    (κ-condensed sets) to avoid universe inconsistencies.
- **Bridging questions**:
  - With A3 (perfectoid): same Scholze school; deep already-known links via
    `Cond(Set) ↔ pro-étale topoi`.
  - With A1 (univalence): "condensed types" — emerging area.
  - With A4 (synthetic Ricci): no obvious bridge yet; potentially
    interesting because Wasserstein space might admit a condensed structure.
