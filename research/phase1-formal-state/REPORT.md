# Phase 1 — Formal-State Inventory (machine-generated draft)

- Generated (UTC): `2026-05-01T00:09:57Z`

## Mathlib4 footprint per seed

### A1 — Univalence / HoTT
Mathlib4 footprint: **NONE**. Mathlib uses classical foundations.
Univalence lives in: Coq UniMath, Agda Cubical, Lean 4 HoTT fork (separate).

### A2 — Condensed Mathematics (34 files in Mathlib/Condensed)

| File | lines | defs | thms | lemmas | TODOs |
|------|-------|------|------|--------|-------|
| `Mathlib/Condensed/AB.lean` | 72 | 0 | 0 | 2 | 2 |
| `Mathlib/Condensed/Basic.lean` | 84 | 0 | 0 | 4 | 0 |
| `Mathlib/Condensed/CartesianClosed.lean` | 18 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Discrete/Basic.lean` | 101 | 6 | 0 | 0 | 0 |
| `Mathlib/Condensed/Discrete/Characterization.lean` | 267 | 0 | 4 | 4 | 0 |
| `Mathlib/Condensed/Discrete/Colimit.lean` | 597 | 27 | 0 | 20 | 0 |
| `Mathlib/Condensed/Discrete/LocallyConstant.lean` | 433 | 19 | 0 | 5 | 0 |
| `Mathlib/Condensed/Discrete/Module.lean` | 287 | 14 | 0 | 0 | 0 |
| `Mathlib/Condensed/EffectiveEpi.lean` | 38 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Epi.lean` | 101 | 0 | 0 | 6 | 2 |
| `Mathlib/Condensed/Equivalence.lean` | 115 | 4 | 0 | 2 | 0 |
| `Mathlib/Condensed/Explicit.lean` | 201 | 6 | 2 | 0 | 0 |
| `Mathlib/Condensed/Functors.lean` | 83 | 5 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/AB.lean` | 39 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/Basic.lean` | 70 | 0 | 0 | 4 | 0 |
| `Mathlib/Condensed/Light/CartesianClosed.lean` | 15 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/EffectiveEpi.lean` | 36 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/Epi.lean` | 154 | 0 | 0 | 5 | 0 |
| `Mathlib/Condensed/Light/Explicit.lean` | 105 | 2 | 1 | 0 | 0 |
| `Mathlib/Condensed/Light/Functors.lean` | 88 | 2 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/Instances.lean` | 48 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/InternallyProjective.lean` | 303 | 1 | 0 | 10 | 0 |
| `Mathlib/Condensed/Light/Limits.lean` | 25 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/Module.lean` | 98 | 3 | 0 | 3 | 0 |
| `Mathlib/Condensed/Light/Monoidal.lean` | 70 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/Sequence.lean` | 362 | 11 | 0 | 14 | 1 |
| `Mathlib/Condensed/Light/Small.lean` | 78 | 2 | 0 | 0 | 0 |
| `Mathlib/Condensed/Light/TopCatAdjunction.lean` | 215 | 12 | 0 | 2 | 0 |
| `Mathlib/Condensed/Light/TopComparison.lean` | 37 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Limits.lean` | 56 | 0 | 0 | 0 | 0 |
| `Mathlib/Condensed/Module.lean` | 83 | 3 | 0 | 1 | 0 |
| `Mathlib/Condensed/Solid.lean` | 87 | 4 | 0 | 0 | 3 |
| `Mathlib/Condensed/TopCatAdjunction.lean` | 216 | 12 | 0 | 2 | 0 |
| `Mathlib/Condensed/TopComparison.lean` | 147 | 2 | 2 | 0 | 0 |

**Notable A2 TODOs (formalization gaps)**
- `Mathlib/Condensed/AB.lean`: TODO: universe levels from type are unified in proof
- `Mathlib/Condensed/AB.lean`: TODO: universe levels from type are unified in proof
- `Mathlib/Condensed/Epi.lean`: TODO: universe levels from type are unified in proof
- `Mathlib/Condensed/Epi.lean`: TODO: universe levels from type are unified in proof
- `Mathlib/Condensed/Light/Sequence.lean`: TODO: make a universe polymorphic `ℕ∪∞` and generalize this result.
- `Mathlib/Condensed/Solid.lean`: TODO (hard): prove that `((profiniteSolid ℤ).obj S).IsSolid` for `S : Profinite`.
- `Mathlib/Condensed/Solid.lean`: TODO (slightly easier): prove that `((profiniteSolid 𝔽ₚ).obj S).IsSolid` for `S : Profinite`.
- `Mathlib/Condensed/Solid.lean`: TODO: This is not the correct definition of solid `R`-modules for a general `R`. The correct one is

### A3 — Perfectoid Spaces (4 files)

| File | lines | defs | thms | lemmas | TODOs |
|------|-------|------|------|--------|-------|
| `Mathlib/RingTheory/Perfectoid/BDeRham.lean` | 99 | 3 | 0 | 0 | 1 |
| `Mathlib/RingTheory/Perfectoid/FontaineTheta.lean` | 213 | 3 | 11 | 0 | 1 |
| `Mathlib/RingTheory/Perfectoid/Untilt.lean` | 79 | 1 | 3 | 0 | 0 |
| `Mathlib/RingTheory/Perfection.lean` | 840 | 21 | 64 | 4 | 1 |

**Notable A3 TODOs (formalization gaps)**
- `Mathlib/RingTheory/Perfectoid/BDeRham.lean`: TODO
- `Mathlib/RingTheory/Perfectoid/FontaineTheta.lean`: TODO
- `Mathlib/RingTheory/Perfection.lean`: TODO

### A4 — Synthetic Ricci
Mathlib4 footprint: **NONE**.
- No CD(K,N), no RCD, no Wasserstein, no Lott-Sturm-Villani.
- `Mathlib/Geometry/Euclidean/MongePoint.lean` is unrelated (classical Euclidean).
- `Mathlib/MeasureTheory/Measure/Tilted.lean` is statistics, unrelated.
- This is one of the largest unformalized active mathematical programs in Mathlib4.

## A1 × A2 frontier — Synthetic Stone Duality

Cherubini-Coquand-Geerligs-Moeneclaey (Dec 2024, arXiv:2412.03203) extend HoTT with **4 axioms** to talk internally about light condensed sets. These are the concrete bridging axioms between A1 (Univalence/HoTT) and A2 (Condensed).

### Axiom — Stone duality
> For any countably presented Boolean algebra $B$, the evaluation map $B\rightarrow 2^{Sp(B)}$ is an isomorphism.

### Axiom — Surjections are formal Surjections
> A map $f:Sp(B')\to Sp(B)$ is surjective if and only if the corresponding map $B \to B'$ is injective.

### Axiom — Local choice
> Whenever $S$ Stone and $E\twoheadrightarrow S$ surjective, then there exists some $T$ Stone, a surjection $T \twoheadrightarrow S$ and a map $T\to E$ such that the following diagram commutes: \begin{equation}\begin{tikzcd} E \arrow[d,""',two heads]\\ S & \arrow[l, "", two heads] T\arrow[lu, ""'] \end{tikzcd}\end{equation}

### Axiom — Dependent choice
> \label{axDependentChoice} Given a sequence of surjections: \begin{center} \begin{tikzcd} X_0 & X_1\arrow[l,""',two heads] & X_2 \arrow[l,""',two heads] & \arrow[l,""',two heads] \cdots \end{tikzcd} \end{center} we have an induced surjection: \begin{center} \begin{tikzcd} X_0 & \arrow[l,""',two heads] \varprojlim X_k \end{tikzcd} \end{center}


## Synthetic Zariski / Stone Duality open questions (verbatim from README)

- Is every étale proposition (formally étale and a scheme) an open proposition?
- Is every étale scheme a sub-quotient of a finite set?
- If $A$ is an étale $R$-algebra (finitely presented and the spectrum is étale),
- Can every bundle (on $Sp A$) of strongly quasicoherent $R$-modules be recovered
- Can we compute some interesting étale/fppf cohomology groups?
- Is the intergral closure of $R$ in a finitely presented $R$-algebra $A$ finitely presented?

## Agda formalization (synthetic-geometry, 12 files)

Formalizes Synthetic Algebraic Geometry over the Zariski topos. **Does not formalize Synthetic Stone Duality** (the condensed side).

| File | lines | postulates |
|------|-------|------------|
| `SyntheticGeometry/Affine.lagda.md` | 194 | 0 |
| `SyntheticGeometry/Divisor.lagda.md` | 66 | 0 |
| `SyntheticGeometry/Open/Properties.lagda.md` | 69 | 0 |
| `SyntheticGeometry/Open.lagda.md` | 98 | 0 |
| `SyntheticGeometry/ProjectiveLine.lagda.md` | 252 | 0 |
| `SyntheticGeometry/ProjectiveSpace/LineThroughPoints.lagda.md` | 279 | 0 |
| `SyntheticGeometry/ProjectiveSpace.lagda.md` | 274 | 0 |
| `SyntheticGeometry/QUESTS/Boundedness.lagda.md` | 40 | 0 |
| `SyntheticGeometry/SQC/Consequences.lagda.md` | 150 | 0 |
| `SyntheticGeometry/SQC.lagda.md` | 71 | 0 |
| `SyntheticGeometry/Spec.lagda.md` | 103 | 0 |
| `SyntheticGeometry/qc-Scheme.lagda.md` | 70 | 0 |

## Formalization-gap shortlist for Phase 2

1. **A2-Solid**: Mathlib's `Mathlib.Condensed.Solid` defines `IsSolid` but carries explicit TODOs for the structure theorems. Concrete formalization gap.
2. **A1×A2 axiom system in Lean**: the four Synthetic Stone Duality axioms are documented in TeX (Cherubini et al. 2024) and partially formalized in Cubical Agda elsewhere, but **not in Lean 4 / Mathlib4**. A minimal axiomatic Lean module could be a clean entry point.
3. **Wärn's anomaly**: Cherubini et al. note that an important property of condensed abelian groups is *not* internally valid (Wärn 2024). Identifying the precise statement and where Mathlib4's external definitions diverge from the internal HoTT view is a candidate for Phase 2.
4. **A3-perfectoid B_dR**: Mathlib4's `BDeRham.lean` has a TODO connecting the explicit theta-mod-p^n construction to the deformation-theoretic / cotangent complex view (Bhatt). This is a known gap pointed at the prismatic line.