/-
# Synthetic Stone Duality — axiomatic skeleton in Lean 4

A self-contained Lean 4 module that mirrors the four axioms of
*A Foundation for Synthetic Stone Duality* by Cherubini, Coquand, Geerligs,
and Moeneclaey (arXiv:2412.03203, Dec 2024) over Lean's classical type theory
(non-HoTT, no `Mathlib` dependency).

This is **not** a HoTT formalization: Lean 4's `Prop` carries proof
irrelevance and the universe of types is not a model of univalence. The
point of this file is the dual experiment proposed in axiom-explorer:

  Take the four bridging axioms identified at the A1 (Univalence) × A2
  (Condensed) frontier, instantiate them on a non-HoTT base, and observe
  which paper-claimed consequences carry over and which require the
  homotopical setting.

The companion finite-model SMT/brute-force verification lives in
`src/axiom_explorer/compute/stone_duality_finite_model.py` (Z3, n=3,4,5).

This file deliberately avoids `Mathlib`. We use only Lean 4 core. Where
the paper relies on a structure already present in Mathlib (e.g. Boolean
algebras), we sketch a minimal abstract version sufficient to state the
axioms.
-/

namespace AxiomExplorer.SSD

-- Disable spurious unused-variable lint inside this file: the eval map
-- intentionally takes both arguments even though one is destructured.
set_option linter.unusedVariables false

universe u

-- We avoid dependence on Mathlib by spelling out the predicates we need.

/-- A function is surjective if every codomain element has a preimage. -/
def Surjective {α : Type u} {β : Type u} (f : α → β) : Prop :=
  ∀ b, ∃ a, f a = b

/-- A function is injective if it preserves distinctness. -/
def Injective {α : Type u} {β : Type u} (f : α → β) : Prop :=
  ∀ ⦃a₁ a₂⦄, f a₁ = f a₂ → a₁ = a₂

/-- A function is bijective if it is both injective and surjective. -/
def Bijective {α : Type u} {β : Type u} (f : α → β) : Prop :=
  Injective f ∧ Surjective f

/--
A minimal abstract Boolean algebra. We do not impose the full equational
theory; for the SSD skeleton we only need a structure name we can quantify
over, and the statement of the four axioms refers to its homomorphisms.
-/
class BooleanAlgebra (B : Type u) where
  zero : B
  one  : B
  meet : B → B → B
  join : B → B → B
  compl : B → B

/--
The two-element Boolean algebra. Concrete model.
-/
def Two : Type := Bool

instance : BooleanAlgebra Two where
  zero := false
  one  := true
  meet := and
  join := or
  compl := not

/--
The "spectrum" of a Boolean algebra: Boolean morphisms `B → 2`. We carry an
abstract `True` placeholder where the structure-preservation lives, so the
type is at the right universe level. Concrete instantiations would specialise
the `True` to actual homomorphism conditions.
-/
def Sp (B : Type u) [BooleanAlgebra B] : Type u :=
  { f : B → Two // True }

/-- The evaluation map `B → 2^{Sp(B)}` of Stone duality. -/
def evalMap (B : Type u) [BooleanAlgebra B] : B → (Sp B → Two) :=
  fun b f => f.val b

/-- A flag identifying countably presented Boolean algebras. -/
class CountablyPresented (B : Type u) extends BooleanAlgebra B where
  cp : Unit := ()

/-
## Axiom 1 — Stone duality

For any countably presented Boolean algebra `B`, the evaluation
map `B → 2^{Sp(B)}` is a bijection.
-/
axiom stoneDuality
  {B : Type u} [CountablyPresented B] :
  Bijective (evalMap B)

/--
The map between spectra induced by a Boolean homomorphism `B → B'`.
Since we do not unfold Boolean-homomorphism structure, `g : B → B'` is taken
as any function for the purposes of this skeleton.
-/
def SpMap {B B' : Type u} [BooleanAlgebra B] [BooleanAlgebra B']
    (g : B → B') : Sp B' → Sp B :=
  fun f' => ⟨fun b => f'.val (g b), trivial⟩

/-
## Axiom 2 — Surjections are formal surjections

A spectrum map `Sp(g) : Sp(B') → Sp(B)` is surjective iff `g : B → B'`
is injective.
-/
axiom surjIffFormalSurj
  {B B' : Type u} [CountablyPresented B] [CountablyPresented B']
  (g : B → B') :
  Surjective (SpMap g) ↔ Injective g

/--
A type is Stone if it is the spectrum of some countably presented Boolean
algebra. We use `Nonempty` of an equivalence to remain proof-relevant only
where it matters.
-/
def IsStone (S : Type u) : Prop :=
  ∃ (B : Type u) (_ : CountablyPresented B), Nonempty (S → Sp B) ∧
    Nonempty (Sp B → S)
  -- We use a back-and-forth pair of maps as a lightweight equivalence stub.

/-
## Axiom 3 — Local choice for Stone spaces

Given a Stone space `S`, a type `E`, and a surjection `p : E → S`, there is
a Stone space `T` with a surjection `q : T → S` and a section-up-to-`p` map
`s : T → E` satisfying `p ∘ s = q`.
-/
axiom localChoiceStone
  {S E : Type u} (hS : IsStone S) (p : E → S) (hp : Surjective p) :
  ∃ (T : Type u) (_ : IsStone T) (q : T → S) (_ : Surjective q) (s : T → E),
    ∀ t : T, p (s t) = q t

/-
## Axiom 4 — Countable dependent choice on surjections

Given an inverse system of surjections `X₀ ↞ X₁ ↞ X₂ ↞ …`, every basepoint
`x₀ ∈ X₀` is reached by a coherent sequence `g(n) ∈ X_n` with `g(0) = x₀`.
This is the countable form of dependent choice the paper requires.
-/
axiom countableDC
  (X : Nat → Type u)
  (f : (n : Nat) → X (n + 1) → X n)
  (hf : ∀ n, Surjective (f n)) :
  ∀ x₀ : X 0, ∃ (g : (n : Nat) → X n), g 0 = x₀ ∧ ∀ n, f n (g (n + 1)) = g n

/-
## Joint type-correctness check

This trivial example asserts the four axiom statements together. If this
file builds, the four axioms are jointly type-correct in Lean 4 core.
-/
example
  {B B' S E : Type u}
  [CountablyPresented B] [CountablyPresented B']
  (g : B → B') (hS : IsStone S) (p : E → S) (hp : Surjective p)
  (X : Nat → Type u) (f : (n : Nat) → X (n + 1) → X n)
  (hf : ∀ n, Surjective (f n)) (x₀ : X 0) :
  Bijective (evalMap B) ∧
  (Surjective (SpMap g) ↔ Injective g) ∧
  (∃ (T : Type u) (_ : IsStone T) (q : T → S) (_ : Surjective q) (s : T → E),
      ∀ t : T, p (s t) = q t) ∧
  (∃ (h : (n : Nat) → X n), h 0 = x₀ ∧ ∀ n, f n (h (n + 1)) = h n) :=
  ⟨stoneDuality,
   surjIffFormalSurj g,
   localChoiceStone hS p hp,
   countableDC X f hf x₀⟩

/-
## Classical-side note

Cherubini et al. derive Markov's principle, ¬WLPO, and LLPO from these
axioms in HoTT. In classical Lean (with `Classical.em`), Markov, ¬WLPO,
and LLPO are *direct* theorems of classical logic; a derivation from
these four axioms is uninformative there.

The genuinely interesting comparative question is: *what extra structure
does adding these axioms commit classical Lean to?* In particular, do
they imply non-trivial constraints on `Type` not derivable from
`Classical.em`?

We leave this for a future iteration. The Lean file here serves as the
*type-correct skeleton* of the four axioms in classical Lean 4.

## See also

- `src/axiom_explorer/compute/stone_duality_finite_model.py` (Z3 sanity).
- `research/phase2-binary-combos/A1xA2/REPORT.md`.
- `research/phase3-deep-dives/C-A1A2-4-lean-skeleton/dossier.md`.
-/

end AxiomExplorer.SSD
