# A1 — Univalence Axiom

- **Branch**: Foundations / Homotopy Type Theory
- **Origin**: Voevodsky, ~2010 (formalized in Coq's UniMath, later Agda Cubical, Lean HoTT).
- **Statement (informal)**: For types `A B`, the canonical map
  `(A = B) -> (A ≃ B)` from identity to equivalence is itself an equivalence.
  Equivalent types are equal.
- **Why productive**:
  - Reorganizes equality at the level of foundations.
  - Makes "transfer along equivalence" automatic — kills boilerplate that ZFC requires.
  - Gives function extensionality and propositional extensionality as theorems.
  - Connects type theory with ∞-groupoids / homotopy theory.
- **Active programs**:
  - **HoTT/UF** community, Cubical type theory (CCHM), Synthetic Homotopy
    Theory, Synthetic Algebraic Geometry over HoTT.
- **Formalization status**:
  - Mature in Coq UniMath, Agda Cubical, Lean 4 HoTT fork (not in Mathlib4
    proper — Mathlib uses classical ZFC-style foundations).
- **Known tensions / non-trivial bits**:
  - Univalence is incompatible with axiom K / UIP.
  - Constructive computational interpretation only fully clean in cubical models.
- **Bridging questions**:
  - Can A2 (condensed) be naturally rephrased in a HoTT setting?
    (Some recent papers do this — Coquand, Cherubini.)
  - Does A4 (synthetic Ricci) admit a HoTT-native phrasing via
    metric-space-as-type with synthetic curvature?
