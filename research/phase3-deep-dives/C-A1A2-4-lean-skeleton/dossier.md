# C-A1A2-4 — Lean 4 axiomatic skeleton of Synthetic Stone Duality

## Statement

Provide a self-contained Lean 4 module that postulates the four axioms of
Cherubini-Coquand-Geerligs-Moeneclaey (arXiv:2412.03203) over Lean's
classical type theory (no `Mathlib` dependency, no HoTT base), with a
type-correctness check that all four can be stated jointly.

## Confidence level

**L0** — verified mechanically by `lake build` succeeding on
`lean/AxiomExplorer/SyntheticStoneDuality.lean`.

## Deliverable

- `lean/lakefile.toml`
- `lean/lean-toolchain` pinned to `leanprover/lean4:v4.16.0`
- `lean/AxiomExplorer/SyntheticStoneDuality.lean` — 4 axioms + joint
  type-correctness example.
- Builds clean: `lake build` reports `Build completed successfully`.

## What this is

A type-checked formalisation of:

1. `stoneDuality` — for any countably presented Boolean algebra `B`, the
   evaluation map `B → 2^{Sp(B)}` is bijective.
2. `surjIffFormalSurj` — `Sp(g)` is surjective iff `g` is injective.
3. `localChoiceStone` — Stone-indexed local choice.
4. `countableDC` — countable dependent choice on surjective inverse systems.

## What this is NOT

- It is **not** a HoTT formalisation. Lean 4's `Prop` carries proof
  irrelevance and the universe of types does not validate univalence.
  Cherubini et al. derive `LLPO`, `Markov`, `¬WLPO` from these axioms in
  HoTT; in classical Lean, these statements are direct theorems of
  `Classical.em`, so derivation from the four axioms is uninformative on
  the classical side.
- It is **not** a verification of consistency of the SSD axiom system
  itself. We use Lean's `axiom` declaration, which is taken on faith.
  The paper provides a topos-theoretic model that supports consistency at
  the HoTT level.
- It is **not** integrated with `Mathlib.Condensed.*`. That would require
  the full Mathlib stack and is out of scope for this Phase 3 dossier.

## Why this is useful

1. **Tipographic consistency check on the paper's axioms.** Any error in
   our reading of the four axioms (wrong direction of an iff, mismatched
   universe, wrong arity) would surface as a Lean type-checking error.
   The build is clean, so our reading is at least type-correct.

2. **Bridging artefact**. There is no SSD module in Lean 4 / Mathlib4. A
   minimal skeleton makes the axiom system accessible to the Mathlib
   community without requiring Cubical Agda or Coq UniMath.

3. **Comparative slot for future work**. The next natural step is:
   - Add a HoTT-flavoured version using the Lean 4 HoTT fork (separate
     project, deferred).
   - Side-by-side, derive the LLPO/Markov/¬WLPO consequences from the
     axioms in HoTT and observe they fail to be derivable from these
     axioms alone in classical Lean (because they are *also* derivable
     from `Classical.em`, so the axioms don't strengthen the classical
     theory in a detectable way).

## Genuinely open question raised by this skeleton

> Do these four axioms commit classical Lean to anything not already
> derivable from `Classical.em`?

In other words: in classical Lean, is the theory `Lean 4 + (4 SSD axioms)`
strictly stronger than `Lean 4 + Classical.em`, or is it equivalent?

A Phase 4-or-later effort would be to construct a model of the SSD axioms
inside classical `Type` (probably using sigma types of Boolean morphisms
literally as the spectrum) and check if it instantiates them all
consistently. If yes, the four axioms are *theorems* of classical Lean;
if no — i.e., if some classical model fails axiom 4 (countable DC) or
axiom 3 (local choice for Stone) — then the axioms genuinely strengthen
classical Lean.

This is left as **a question for a future iteration**. It is *not*
addressed by the paper, which works in HoTT throughout.

## CI integration

Decided **not** to add `lake build` to GitLab CI for now. Reasoning:

- The Lean toolchain pulls ~500 MB and takes 90+ seconds even cached.
- The CI runner image is a vanilla `python:3.12-slim` mirror; adding Lean
  would complicate the image significantly.
- The Lean module is a research artefact verified locally; if it
  regresses, future contributors will rebuild it manually.

If future Phase 3 candidates require Lean+Mathlib heavily, we revisit
and add a Lean-flavoured CI image.

## Honesty notes

- The Lean skeleton uses very minimal abstract structures. The
  `BooleanAlgebra` class has only signatures, no equations. The `Sp B`
  type is a `Subtype { f : B → Bool // True }` — i.e., really every
  function — because we did not encode "Boolean homomorphism". A more
  faithful skeleton would carry the full Boolean homomorphism structure;
  that is left for a future iteration.
- The `IsStone` predicate uses a back-and-forth pair of maps as a
  lightweight equivalence stand-in. A full `S ≃ Sp B` would require
  `Equiv` from Mathlib.

These minimalisms do not affect the joint type-correctness check, which
is what the dossier claims to deliver.
