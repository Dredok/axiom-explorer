# C-A2A3-2 — Cardinality scaling of the condensed fundamental group

## Statement (candidate, L3)

Let `X` be a smooth quasi-projective variety over a field `k` of cardinality
`κ`. Then the underlying group of the condensed fundamental group satisfies
the cardinality bound

    |π_1^{cond}(X_k, x̄)(*)|  ≤  max(κ^{ℵ_0},  2^κ).

Under standard cardinal arithmetic, for infinite `κ` this collapses to
`2^κ`, i.e., the next level of the beth hierarchy above `|k|`.

For "nontrivial" inputs (e.g., `X` with a nonzero étale H_1 over Z_l for
some `l`, or `X` of the form `A^1_k ∖ S` with `S ≠ k`), the bound is
**attained** (equality, up to a finite/countable correction).

## Confidence level

**L3 — speculative pattern**.
- Matches the two cases the paper explicitly attests: `P^1_C` and `P^1_Q`
  (Remark 7.14 of arXiv:2510.07443).
- Not derived in the paper.
- Not verified beyond those two cases.
- Falsifiable: a future computation (or a careful reading of the paper's
  later sections we did not parse) could produce a `(X, k)` with
  `|π_1^{cond}|` exceeding `2^κ`.

## Why this is interesting

The classical étale fundamental group is **insensitive** to the cardinality
of the base field for fixed `X` (e.g., `π_1^ét(P^1_k) = 1` for any
separably closed `k` with `char(k) = 0`). The pro-étale group of
Bhatt-Scholze is also insensitive in the same sense.

The paper observes that `π_1^{cond}` *is* sensitive: it returns different
groups (different cardinalities, different structure) for `X_C` vs. `X_Q`
even though both fields are countably or continuum-large.

The candidate pattern says: the *cardinality envelope* of this sensitivity
is uniform across schemes — it is the next beth level above `|k|` — and is
realised (with equality) for X with non-trivial first homology.

## Numerical evidence

We implemented `axiom_explorer.compute.condensed_pi1_cardinality` which
encodes the paper's two attested cases and the candidate pattern's
prediction:

| Scheme | Field | Card(k) | Paper bound | Pattern prediction | Match |
|--------|-------|---------|-------------|--------------------|-------|
| P^1 | C | continuum (c) | beth_2 = 2^c | beth_2 | ✓ |
| P^1 | Q | aleph_0 | c = 2^aleph_0 | c | ✓ |
| A^1 \ S | C | c | beth_2 (struct.) | beth_2 | ✓ (qualitative) |

Three predictions for unattested cases (waiting for falsification):

| Scheme | Field | Card | Pattern says |
|--------|-------|------|--------------|
| P^1 | F̄_p | aleph_0 | c |
| P^1 | Q̄ | aleph_0 | c |
| A^1 | C_p | c | beth_2 |
| Elliptic curve | C | c | beth_2 |
| Elliptic curve | Q | aleph_0 | c |
| Elliptic curve | F̄_p | aleph_0 | c |

## Why we believe this is a structural pattern, not coincidence

The paper's argument for `|π_1^{cond}(P^1_C)| = 2^c` proceeds in two
bounds:

- **Lower bound** via the surjection from `Galκ(η) ≃ F̂r_C` onto a quotient
  of size `2^c` (the product of cZ_hat modulo the direct sum).
- **Upper bound** via `|F̂r_C| ≤ |C|^{aleph_0} = c^{aleph_0} = 2^c` for `C`
  uncountable, and by `|F̂r_Q| ≤ |Q|^{aleph_0} = aleph_0^{aleph_0} = c` for
  `Q` countable.

Both bounds are functions only of `|k|`. The product structure of the
quotient (size `2^c` not `c`) reflects the **uncountable family of normal
subgroups closed under the natural topology** that exist over `C` but not
over `Q`. This phenomenon scales with `|k|` because the family is
indexed by `k`. Under the natural cardinal arithmetic, the upper-bound
side is `|k|^{aleph_0}` and the lower-bound side is `2^{|k|}`, giving the
`max(κ^{aleph_0}, 2^κ)` form.

So the pattern follows from the **shape of the paper's argument**, not from
specific facts about `P^1`. If the argument transfers (which is plausible
for any X whose Galois group of the generic point is non-trivial and
indexed by `k`), the pattern holds.

## How this could be falsified

1. A Mathlib4 or Lean computation of `π_1^{cond}` for some explicit
   curve over a non-trivial field might exhibit a cardinal beyond
   `max(κ^{ℵ_0}, 2^κ)`. We could not construct such a counterexample.

2. The paper itself, or a follow-up, might prove that for some restricted
   scheme class, `|π_1^{cond}|` is bounded by a *strictly smaller*
   cardinal — that would refine, not contradict, the bound.

3. A computation involving `π_n^{cond}` for `n ≥ 2` might produce a
   structure whose underlying-group-at-π_1 exceeds the predicted bound.

## Honesty notes

- We did not implement an actual computation in any non-trivial case;
  the harness only tracks cardinal-level bounds symbolically.
- The "quasi-projective" hypothesis is informal; the paper works with
  qcqs schemes more generally and we have not checked if the bound
  needs adjustment for non-qcqs cases (it should not, but we did not
  verify).
- We did not read all 103 pages of arXiv:2510.07443 — only the
  introduction, §7.1-7.4 and the cardinality remarks. A close reading
  might reveal an explicit proof of the pattern or a sharper bound.

## Phase 4 candidate test

If the orchestrator advances this to a Phase 4 test, the cleanest move
would be:

1. Email the authors of arXiv:2510.07443 with the conjectured pattern,
   citing this dossier and the agreement with their two attested cases.
   Ask whether they have an internal computation that confirms or refutes
   it.
2. Compile a Lean statement of the bound (not the proof) that could be
   checked against any concrete `π_1^{cond}` computation that lands in
   Mathlib later.

## Related candidate (cross-pair)

The Wärn obstruction to internal projectivity of `Z[N_∞]` in condensed
abelian groups (raised in C-A1A2 dossier) involves a similarly structural
cardinality issue — `N_∞` is countable but its internal type-theoretic
behaviour distinguishes it from finite truncations only at infinity.
There may be a unifying theme: **condensed structures track cardinal
information that classical / étale structures coarse over**. This is
a Phase 4 question.
