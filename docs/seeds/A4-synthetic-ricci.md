# A4 — Synthetic Ricci Curvature (LSV / CD(K,N))

- **Branch**: Analysis / Metric Geometry / Optimal Transport
- **Origin**: Lott–Sturm–Villani, 2006–2009. CD(K,N) condition.
- **Statement (informal)**: For a metric measure space (X, d, m), one
  defines `CD(K, N)` by **convexity properties of entropy along
  Wasserstein geodesics** of probability measures on X. For smooth
  Riemannian manifolds, `CD(K, N)` is equivalent to:
  Ricci curvature ≥ K and dimension ≤ N.
- **Why productive**:
  - Extends Ricci-curvature-based theorems (Bonnet-Myers, Bishop-Gromov,
    Levy-Gromov, Brunn-Minkowski) to **non-smooth** metric measure spaces.
  - Sturm's CD(K,∞) and the refined RCD spaces (with infinitesimal
    Hilbertian condition) bridge analysis and metric geometry.
  - Used in: Cheeger-Colding theory, structure of limits of manifolds with
    Ricci bounds, GH-convergence of metric measure spaces.
- **Active programs**:
  - RCD theory, structure theory of RCD(K,N) spaces, sub-Riemannian and
    sub-Finsler synthetic curvature, optimal transport on graphs/discrete
    spaces (Erbar-Maas).
- **Formalization status**:
  - Mathlib4 has parts of measure-theoretic optimal transport.
    Synthetic Ricci itself is largely unformalized.
- **Known tensions / non-trivial bits**:
  - Local-global tension: CD(K,N) is a global notion via geodesics, not a
    pointwise condition.
  - Equivalent reformulations (entropy, Bochner, gradient flow) require
    work to identify.
- **Bridging questions**:
  - With A1 (univalence): metric-spaces-as-types with synthetic curvature.
    Likely sparse.
  - With A2 (condensed): could optimal transport be redone in condensed
    framework? Probably sparse and possibly fertile.
  - With A3 (perfectoid): essentially no contact. Adelic/p-adic optimal
    transport exists in tiny corners but not connected to perfectoid theory.
