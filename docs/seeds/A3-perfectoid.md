# A3 — Perfectoid Spaces

- **Branch**: Arithmetic Geometry / p-adic Hodge theory
- **Origin**: Peter Scholze, 2012 (PhD thesis).
- **Statement (informal)**: A perfectoid space over a perfectoid field K of
  characteristic 0 has a *tilt* — a perfectoid space K♭ over a perfectoid
  field of characteristic p — and the étale topoi are equivalent.
- **Why productive**:
  - Solved long-standing conjectures: weight-monodromy in many cases,
    p-adic Hodge theory simplifications, almost purity.
  - Underpins: prismatic cohomology (Bhatt-Scholze), local-global Langlands
    geometric, integral p-adic Hodge theory.
- **Active programs**:
  - Prismatic cohomology, q-de Rham, condensed × perfectoid (Scholze),
    geometric Langlands.
- **Formalization status**:
  - `perfectoid-spaces` Lean project (Buzzard, Massot, Commelin) is a
    landmark formalization of the *definition* of a perfectoid space.
    The deep theorems are not yet formalized.
- **Known tensions / non-trivial bits**:
  - Perfectoid hypothesis is restrictive; many natural rings don't satisfy it.
  - Tilting is functorial but not always easy to compute.
- **Bridging questions**:
  - With A2 (condensed): deep, known. Diamonds (Scholze) are condensed-style
    objects that generalize perfectoid spaces.
  - With A1 (univalence): minimal direct contact. Possible angle via
    synthetic algebraic geometry over HoTT.
  - With A4 (synthetic Ricci): essentially zero direct contact in the
    literature — sparse frontier.
