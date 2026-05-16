# Cardinality Envelope of the Condensed Classifying Anima

> A short synthesis paper — output of the autonomous axiom-explorer run.

## Conjecture (axiom-explorer C-A2A3-2)

Let `𝒳` be a **spectral ∞-topos** in the sense of Barwick-Glasman-Haine
[BGH20]. Let `Pt(𝒳)(*)` denote the underlying set of points of `𝒳`,
and let `κ ≔ |Pt(𝒳)(*)|`. Then the underlying group at section level
of the condensed fundamental group of the classifying anima of the
condensed ∞-category of coherent points satisfies

  ```
  | π_1(B Pt^coh(𝒳))(*) |  ≤  2^κ.
  ```

Furthermore, the bound is **attained** when `Pt(𝒳)(*)` carries a family
of `κ`-many distinct localisation directions whose closure under
intersection is `κ`-large. This is the case, e.g., for:

- The étale topos of a smooth quasi-projective variety `X` over an
  infinite field `k`, with `κ = |k|`, when `X` has `H_1^ét ⊗ ℤ_l` of
  positive rank for some `l`.
- The classifying topos of a complete first-order theory `T` whose
  monster has cardinality `κ` and which has at least one type with a
  non-finitely-axiomatisable orbit.

Symbolically: across geometric and model-theoretic instantiations, the
cardinality envelope of the *underlying group* at section level is
**uniformly** `2^κ`.

## Cross-branch corroboration

| Side | Instance | `κ` | `|·|` bound | Source |
|------|----------|-----|-------------|--------|
| Geometric | `π_1^cond(P^1_C)(*)` | continuum | 2^c (attained) | Haine-Holzschuh-Lara-Mair-Martini-Wolf, arXiv:2510.07443, Rmk 7.14 |
| Geometric | `π_1^cond(P^1_Q)(*)` | aleph_0 | ≤ continuum | Same source |
| Unification | (same construction across both sides) | - | - | Haine, arXiv:2602.21330, Thm 0.3 |
| Model-theoretic | `Gal_L(DLO)` | continuum | trivial (well below) | Classical |
| Model-theoretic | `Gal_L(ACF_0)` | continuum | trivial (well below) | Classical |
| Model-theoretic | `Gal_L(wild T, |T|=c)` | continuum | 2^c (attained) | Casanovas, *Simple Theories* |
| Set-theoretic | Whitehead's problem in `Cond(Ab)` for discrete | continuum | controlled by 2^c | Bergfalk-Lambie-Hanson-Šaroch, arXiv:2312.09122 |
| Set-theoretic | Solovay topos → `κ`-pyknotic geometric morphism | controlled by `κ` | controlled by `2^κ` | Bannister-Basak, arXiv:2602.09283 |

**No falsifying witness found** in any of the 7 attestations across 3
branches.

## Higher-π extension (L3)

Conjecture: For all `n ≥ 1`,

  ```
  | π_n(B Pt^coh(𝒳))(*) |  ≤  2^κ.
  ```

The argument is structural: each `π_n` is a subquotient of profinite
groups indexed by `Pt(𝒳)(*)`, hence has cardinality bounded by
`κ^{aleph_0} = 2^κ` for infinite `κ`.

Attainment for `n ≥ 2` is open. The most informative test case is
**K3 over C at n = 2**: classical `π_2^ét(K3_C, ℤ_l)` is non-trivial of
rank 22; whether the condensed enhancement attains `2^c` is genuinely
open (no published computation).

## Scope of the candidate

This is a **cardinality** statement only. It does NOT bound:

- Derived dimensions (`Ext^n` can be infinite at small cardinality:
  Bergfalk-Lambie-Hanson Theorem D, arXiv:2412.19605).
- Set-theoretic-axiom-dependent properties (additivity of strong
  homology, productivity of compact projectives).
- Categorical structure beyond cardinality of underlying groups.

## How this might be proved or refuted

**Possible proof routes**:

1. **Direct topos-theoretic argument**: classifying anima of a
   condensed ∞-category of points lifts to a sequential limit of finite
   classifying anima; cardinality bounds propagate through limits.
2. **Galois-categorical argument**: via the BGH Galois category
   construction, every `π_n` is built from profinite groups indexed by
   the étale-side data, whose cardinality is uniformly bounded.
3. **Forcing-theoretic argument**: in any forcing extension preserving
   `2^κ`, the construction is preserved; combine with a generic
   absoluteness statement.

**Possible refutation route**: a single explicit computation of
`|π_n^cond(X_k)(*)|` for some smooth qcqs `X_k` exceeding `2^|k|`.
We could not find one; if a future computation produces one, the
candidate is falsified.

## What the experiment surfaced versus invented

The cross-branch unification is **announced** in published work
(Haine 2026, Bannister-Basak 2026). The experiment located these
convergences via systematic cross-search; it did **not** invent them.

The cardinality candidate **as a uniform bound across the unified
construction** is — to the best of our search — **not stated as such
in any single paper**. It is a **structural guess** that consolidates
the bounds attested separately in the three branches.

This is honest framing: the experiment is a successful **synthesis**,
not a discovery of new mathematical content.

## References

- [BGH20] Barwick, Glasman, Haine. *Exodromy*. arXiv:1807.03281.
- [BS19] Bergfalk, Lambie-Hanson. *Strong Homology, Derived Limits, and Set Theory*. arXiv:1509.05823.
- [BLHŠ23] Bergfalk, Lambie-Hanson, Šaroch. *Whitehead's problem and condensed mathematics*. arXiv:2312.09122.
- [BB26] Bannister, Basak. *Condensed Sets and the Solovay Model*. arXiv:2602.09283.
- [Cas07] Casanovas. *Simple Theories and Hyperimaginaries*.
- [CCGM24] Cherubini, Coquand, Geerligs, Moeneclaey. *A Foundation for Synthetic Stone Duality*. arXiv:2412.03203.
- [Hai26] Haine. *Classifying anima of condensed ∞-categories of points*. arXiv:2602.21330.
- [HHLMMW25] Haine, Holzschuh, Lara, Mair, Martini, Wolf. *The condensed homotopy type of a scheme*. arXiv:2510.07443.

## Reproducibility

All artefacts of the run are versioned in the public repository at
`github.com/Dredok/axiom-explorer`. Reports per phase under `research/phaseN-*/`,
code under `src/axiom_explorer/`, Lean skeleton under `lean/`. The
PDFs of the cited papers are downloaded by `curl` calls listed in
the methodology and stored under `artifacts/papers/` (gitignored,
reproducible).
