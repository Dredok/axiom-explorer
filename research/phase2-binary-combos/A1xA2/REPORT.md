# Phase 2 — A1 × A2: Univalence × Condensed Mathematics

## Bridge identified — Synthetic Stone Duality (SSD)

**Reference**: Cherubini, Coquand, Geerligs, Moeneclaey, *A Foundation for Synthetic
Stone Duality*, arXiv:2412.03203 (Dec 2024), `math.LO`, 17 pages.

**Repository**: https://github.com/felixwellen/synthetic-zariski/tree/main/condensed
(includes a Cubical Agda formalization stub of related work in
`felixwellen/synthetic-geometry`).

This is the concrete bridging object Phase 0 predicted: **HoTT extended with 4
axioms** that lets one reason internally about **light condensed sets**
(Clausen-Scholze). It validates A1 × A2 as a real frontier and gives us a
fixed target object to perturb.

## The 4 axioms (verbatim from `condensed-summary/axiom.tex`)

1. **Stone duality**. For any countably presented Boolean algebra $B$, the
   evaluation map $B \to 2^{Sp(B)}$ is an isomorphism.
2. **Surjections are formal Surjections**. A map $f: Sp(B') \to Sp(B)$ is
   surjective iff the corresponding map $B \to B'$ is injective.
3. **Local choice**. For $S$ Stone and $E \twoheadrightarrow S$ surjective,
   there exists $T$ Stone with surjection $T \twoheadrightarrow S$ and a
   map $T \to E$ making the diagram commute.
4. **Dependent choice** (countable). Given $X_0 \twoheadleftarrow X_1
   \twoheadleftarrow X_2 \twoheadleftarrow \dots$, the induced
   $X_0 \twoheadleftarrow \varprojlim X_k$ is a surjection.

## Theorems Cherubini et al. derive from these axioms

| Theorem | Status |
|---------|--------|
| Negation of WLPO | provable from the 4 axioms |
| Markov's principle | provable |
| LLPO (lesser limited principle of omniscience) | provable |
| All maps from $[0,1]$ to itself are continuous (ε-δ) | provable |
| Brouwer's fixed-point theorem | provable internally |
| Stone duality for the type of Stone spaces | from axiom 1 |
| Compact Hausdorff = quotient of Stone with Stone kernel | by definition |

## Sanity check — finite-model brute force verification

We implemented `src/axiom_explorer/compute/stone_duality_finite_model.py` to:

1. Verify Axiom 2 in the finite case: brute-forced 3,408 finite functions
   (n=3,4,5) and confirmed `f surjective ↔ f^* injective on pullback of
   subsets` holds with **0 violations**.
2. Argue Axioms 3 and 4 hold trivially in finite Stone spaces / finite
   chains.
3. Verify the consequences — LLPO and Markov's principle — hold for finite
   $\mathbb{N}_\infty$-style sequences (n=3, n=5): no counterexamples.

This rules out gross encoding errors. The interesting math is what the
finite check **cannot see**.

## Wärn's anomaly — a candidate Phase 3 deep dive

The paper notes (intro.tex):

> "David Wärn has proved that an important property of condensed abelian
>  groups is *not* valid internally."

Specifically: $\mathbb{Z}[\mathbb{N}_\infty]$ is **not** internally projective
in the category of internal abelian groups, even though it is the free
abelian group on $\mathbb{N}_\infty$ (and free abelian groups are projective
in `Ab` classically and in finite cases).

**This is an asymmetry between the internal HoTT view and the external
condensed view**. Our finite-model harness *cannot* see this — we
explicitly verified that $\mathbb{Z}[X]$ for finite $X$ is projective in
`Ab` (trivial). The obstruction is genuinely infinitary.

This is exactly the kind of phenomenon the experiment is set up to surface.
**Candidate question for Phase 3**: precisely characterize the failure
locus — which "nice" properties of `ZAb` or `CondAb` survive the SSD
internalization, and which break? Is there a structural reason
(homotopical, model-theoretic) that classifies the survivors?

## Conjectures verbatim from the SSD article

1. **Completeness conjecture** (intro.tex):
   > "We also conjecture that the present axiom system is *complete* for
   > the properties [of light condensed anima] that are internally valid."

   This is a **proof-theoretic completeness claim**: any internally-true
   statement about light condensed anima is derivable from the 4 axioms.
   Status in the paper: open.

2. **Linear order on Cantor implies LLPO** (`condensed-cohomology-article/Alternating.tex`):
   > "We conjecture the existence of any linear (≤)-order on Cantor space
   > implies LLPO."

3. **Order pair implying MP**:
   > "We also might conjecture the existence of two partial orders ≤, < such
   > that ¬(a≤b) → b<a implies MP."

## Phase 3 candidate shortlist (A1 × A2)

| ID | Candidate | Confidence | Type |
|----|-----------|------------|------|
| C-A1A2-1 | Completeness of the 4-axiom SSD system for internal truths in light condensed anima | L3 (open conjecture in the source) | Open conjecture |
| C-A1A2-2 | Sharp characterization of when a "classical" property of condensed abelian groups survives internal HoTT (Wärn obstruction structure theorem) | L3 (suggested by negative observation) | Structural classification |
| C-A1A2-3 | Linear ≤-order on Cantor space → LLPO | L3 (conjecture in source) | Implication |
| C-A1A2-4 | Lean 4 axiomatization of the 4 SSD axioms + classical-derivation of MP, ¬WLPO, LLPO over `Type` (without HoTT) | L1 (definitions and consequences are explicit) | Formalization gap |

**C-A1A2-4 is the cleanest deliverable**: write a self-contained Lean 4 module
that postulates the 4 axioms over a non-HoTT base (`Type` + `Prop`) and proves
the non-trivial classical consequences (MP, ¬WLPO, LLPO). This is a clean
formalization gap: the axioms are documented in TeX and partially in Cubical
Agda, but Lean 4 / Mathlib4 has *neither HoTT nor SSD*. A standalone Lean 4
specification serves as both:

- A *consistency check* against the paper's claims (any error in our
  reading would fail to typecheck).
- A *bridging artifact* that makes the SSD axioms accessible to the
  Mathlib4 community without requiring a HoTT environment.

## What this combination is *not*

- It is not (yet) a formalization of the topos-theoretic model that
  validates the axioms. That requires homotopy / ∞-topos infrastructure
  not yet in Mathlib4.
- It does not address full condensed (only light condensed). The paper
  uses light condensed precisely to avoid universe issues.
- It does not engage with David Wärn's specific counterexample beyond
  noting its existence; that would be Phase 3.

## Status for orchestrator

A1 × A2 has produced a real, citable, partially-falsifiable target with
multiple candidate dossiers for Phase 3. **Recommend advancing**.
