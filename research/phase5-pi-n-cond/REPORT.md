# Phase 5 — Higher condensed homotopy (extension of C-A2A3-2)

## Motivation

Phase 4 closed with a clean L2-strong candidate for the cardinality
envelope of `π_1^{cond}`. Haine et al. arXiv:2510.07443 work explicitly
through `π_0^{cond}` (Theorem 1.6) and `π_1^{cond}` (Theorems 1.8-1.13).
The higher π_n's, n ≥ 2, are **implicit** in their framework — the
condensed homotopy type `Π_∞^{cond}(X)` is a full anima, hence carries
all higher homotopy — but **no theorem in the paper explicitly addresses
their cardinality, structure, or relationship to classical étale higher
homotopy**.

This Phase 5 extends C-A2A3-2 to higher π_n's and identifies the most
informative test case.

## Candidate (L3)

For X smooth qcqs over an infinite field k of cardinality κ:

    |π_n^{cond}(X_k, x̄)(*)|  ≤  2^κ   for all n ≥ 1.

**Reasoning** (structural, not a proof):

1. `Π_∞^{cond}(X) ≃ B Pt^{coh}(X_ét)` (Haine arXiv:2602.21330 Theorem 0.3
   for the spectral case).
2. Each `π_n` of the condensed classifying anima is a subquotient of
   profinite groups indexed by closed points of X.
3. The cardinality of any such profinite group is bounded by
   `|index|^{ℵ_0} = κ^{ℵ_0} = 2^κ` for infinite κ.

The bound applies **uniformly across n**. Attainment for `n ≥ 2`
depends on whether the higher étale homotopy of X carries enough
structure indexed by closed points to saturate the cardinality.

## Why this matters

If true, the statement says:

> The condensed enhancement of the étale homotopy type adds at most
> one beth level of cardinality at each n, never more. This is a
> *uniform* bound across the entire homotopy tower.

This would be the first uniform-across-n statement we've seen in this
area, and would consolidate the C-A2A3-2 candidate into a richer
theorem-shape.

## Most informative test case — K3 surface, n=2

K3 surfaces over C have:

| Invariant | Value |
|-----------|-------|
| `π_1^ét(K3_C)` | trivial |
| `π_2^ét(K3_C, ℤ_l)` | non-trivial; rank 22 (related to H_2 of K3) |
| `H_2(K3_C, ℤ)` | ℤ^22 (lattice of signature (3,19)) |

Our Phase 5 candidate predicts:

    |π_2^{cond}(K3_C, x̄)(*)|  ≤  2^c.

The interesting question is **attainment**:

> Does `π_2^{cond}(K3_C)` saturate to `2^c`, or does the rank-22
> classical structure persist as a "small" countable-rank-22 subgroup
> of an `at most 2^c`-large condensed enhancement?

Three possible scenarios:

1. **Trivial enhancement**: `π_2^{cond}(K3_C, *)(*)` ≃ classical
   `π_2^ét(K3_C, x̄)`, i.e., a profinite group of countable rank,
   well below `2^c`.
2. **Modest enhancement**: condensed adds a `c`-sized correction
   (continuum but not its powerset), saturating the bound at the
   level of `c` not `2^c`.
3. **Full saturation**: `π_2^{cond}` reaches `2^c`, mirroring `π_1`'s
   behaviour.

Which scenario holds is the **first genuinely open question** at this
intersection that we identified: it would refine our candidate envelope
from "always ≤ 2^κ" to a more precise statement about **when each π_n
attains it**.

## What machinery would resolve K3 n=2

Following the Haine et al. argument for π_1:

1. Identify the appropriate Galois category `Gal(K3_C)` whose classifying
   anima recovers `Π_∞^{cond}(K3_C)`.
2. Compute the homotopy 2-truncation of this classifying anima.
3. The 2-truncation of a category C admits a comparison with the étale
   higher fundamental groupoid. The cardinality of `π_2(BC)(*)` at section
   level can be read off from the 2-truncation.

For K3 specifically, K3 is **simply connected** (étale), so `Gal(K3_C)`
is concentrated in higher data. The interesting question is whether the
condensed enhancement promotes the discrete `π_2^ét = ℤ_l^22` to a
condensed group of larger cardinality.

We **cannot resolve this in this run**. It requires:
- Either a Lean / Agda computation against the formal definitions
  (Mathlib4 currently has no `π_n^{cond}` infrastructure beyond the
  basic condensed sheaves).
- Or expert knowledge of the BGH Galois category for K3, which is
  not present in our harness.

It is left as the **cleanest open question** for Phase 6 / future
human work.

## Status

L3 prediction of the envelope `|π_n^{cond}| ≤ 2^|k|` for all n ≥ 1.
Open: K3 n=2 attainment scenario. No falsifying evidence found in
arXiv (search found 0 papers on "condensed K3", "proetale K3",
"higher condensed homotopy" — the area is genuinely virgin for
n ≥ 2 + non-trivial higher homotopy).

This Phase 5 dossier is **the cleanest forward question** the
experiment surfaces: a falsifiable, well-posed L3 question whose
answer would refine the central L2 candidate of the run.


---

## Update — derived-limit constraints (Bergfalk-Lambie-Hanson)

After writing the dossier, I read deeper into Bergfalk-Lambie-Hanson
arXiv:2412.19605 ("Infinitary combinatorics in condensed math and
strong homology"). Their Theorems A-D are concrete constraints on the
infinitary structure of Cond(Ab):

- **Theorem A** (ZFC): the natural functor `Pro(D(Ab)) → D(Cond(Ab))`
  is not full. Specifically:
  ```
  RHom_{Pro(D≥0(Ab))}(∏ ⊕ Z, Z) ≠ RHom_{D≥0(Cond(Ab))}(∏ ⊕ Z, Z)
  ```
  The first is concentrated in degree 0, the second is not.

- **Theorem D** (ZFC): for any S, T ∈ ED that are Čech-Stone of
  discrete sets of cardinality ≥ ℵ_ω, the constant sheaf K (any
  field) on S × T has **infinite injective dimension**. Hence
  compact-projective condensed anima are not closed under products.

### How this relates to the candidate envelope

Bergfalk-LH constrain the **derived/extension structure** of Cond(Ab),
not directly the cardinality of homotopy groups π_n^{cond}. The two
are different invariants:

- Our envelope: `|π_n^{cond}(X_k)(*)| ≤ 2^|k|`. About cardinality.
- Bergfalk-LH: dimensions of `Ext^n` groups can be infinite, certain
  natural functors are not full. About structure.

These two statements are **compatible**: a homotopy group of cardinality
≤ 2^|k| can perfectly well give rise to an Ext-tower of infinite
dimension. The cardinality envelope does not constrain dimensions.

### Caveat the Bergfalk-LH results introduce

Their results show that **straight cardinality bounds may underestimate
the "actual structural complexity"** of condensed mathematics. Two
condensed groups of the same cardinality can have completely different
derived-category behaviour; one finite-injective-dim, the other
infinite. So while the candidate envelope on |π_n^{cond}| might be
true, it is also a **coarse invariant** — useful as an upper bound, but
not the deepest layer of structure.

This is honest reporting: the cardinality pattern is a **first-order
structural observation**, not the whole story. The full picture
includes derived/extension dimensions which can be infinite even at
small cardinalities.

### Stronger statement that would survive both

> For X smooth qcqs over an infinite field k of cardinality κ, every
> π_n^{cond}(X_k, x̄) is an inverse limit of profinite groups indexed
> by closed points of X, hence has cardinality ≤ 2^κ. The derived
> structure (Ext-towers, dimensions) is **not** bounded by such a
> coarse rule and can grow with cardinality of the parameter index.

This refines the candidate to a more honest position: the envelope
applies to **cardinality only**, and the deeper structure (derived
limits, injective dims, additivity of strong homology) is genuinely
sensitive to set-theoretic axioms (Theorem B of Bergfalk-LH is
consistent under specific cardinal assumptions; not provable in ZFC
alone).

This is **not a refutation** of the candidate — it is a refinement to
its appropriate scope.
