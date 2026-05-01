# Structural argument supporting the cardinality envelope

## Goal

Sketch why the candidate pattern `|π_1^{cond}(X_k)(*)| ≤ 2^|k|` (with
equality often attained) is **structural**, not specific to `P^1`.

## The mechanism in Haine et al. for P^1 \ S

(Synthesizing §7.1 of arXiv:2510.07443.)

1. **Galois group of the generic point**: for `X = A^1_C \ S` with `S ⊂ C`,
   the absolute Galois group of `κ(η) = C(T)` is the free profinite group
   `F̂r_C` on the underlying set `C`.
   - Cardinality: `|F̂r_C| ≤ |C|^{ℵ_0} = 2^c`.

2. **The condensed π_1**: by Proposition 7.2, there is a short exact
   sequence of abstract groups:
   ```
   1 → N_S → F̂r_C → π_1^{cond}(A^1_C \ S, η̄)(*) → 1
   ```
   where `N_S` is the abstract normal closure of the subgroups `Ẑ(a)` for
   all `a ∈ C \ S`.

3. **Lower bound on the quotient**: the canonical map
   ```
   F̂r_C → ∏_{a∈C} Ẑ
   ```
   factors through `π_1^{cond}(A^1_C \ S, η̄)(*)` and surjects onto a
   quotient of size `|∏ Ẑ| / |⊕ Ẑ|` = `2^c / c` = `2^c`.

4. **Conclusion for P^1**: `|π_1^{cond}(P^1_C)(*)|` is sandwiched between
   `2^c` (lower) and `2^c` (upper), so equals `2^c`.

## Why the same envelope applies to general qcqs schemes

The **only inputs** to the cardinality argument are:

| Step | Input | Cardinality contribution |
|------|-------|--------------------------|
| 1 | Galois group of the generic point | `|F̂r_k| ≤ |k|^{ℵ_0} = 2^|k|` for infinite k |
| 2 | Short exact sequence of (abstract) groups | Cardinality of quotient ≤ that of numerator |
| 3 | Surjection to product over an index of size `|k|` | Lower bound `2^|k|` if the index is `|k|` |

For a smooth qcqs scheme `X` over `k`:

- The Galois group of the generic point `Gal(κ(η_X))` is bounded above
  by `|F̂r_k|` (for X separated, finite type) since `κ(η_X)` is a finite
  extension of `k` adjoined with a finite-degree transcendental, whose
  absolute Galois group is built from the absolute Galois of `k` and a
  free profinite contribution indexed by closed points.
- The condensed π_1 is a quotient (Galois-theoretic) of this group.
- The **index of the relevant product family** in the lower-bound is
  bounded above by the number of closed points of `X`, which is
  `≤ |k|` for `X` finite type.

So both the upper and lower bounds scale as `2^|k|`. The envelope
`max(|k|^{ℵ_0}, 2^|k|) = 2^|k|` (for infinite `k`) is therefore a
**uniform structural bound** for finite-type smooth schemes over an
infinite field.

## What this argument does NOT prove

- It does not prove the **lower bound** is attained for **every**
  finite-type smooth scheme. P^1 attains it; for `X` with trivial étale
  fundamental group and no rational points missing, the lower bound
  computation may collapse.
- It does not extend to non-finite-type schemes or non-smooth schemes
  where the Galois of the generic may differ.
- It does not give finer information about the **structure** of the
  condensed π_1 (it only bounds cardinality).

## Sufficient condition for attainment

The lower bound `2^|k|` is attained as soon as the scheme `X` has a
non-trivial homomorphism `Gal(κ(η)) → ∏_{i ∈ |k|} G_i` for some
profinite `G_i` that does not factor through the direct sum. This is
ensured, e.g., when `X` has a closed-point structure indexed by `|k|`
points with non-trivial residue Galois action (which is typical for
geometrically connected smooth quasi-projective schemes over `k`).

For `X = P^1` over an infinite separably closed `k` of characteristic 0,
attainment is direct from the proof.

## Cross-branch implication

Under Haine arXiv:2602.21330 Theorem 0.3, the same argument applies on
the model-theoretic side:

- `Gal(κ(η))` becomes the absolute Galois group of the monster's
  language, bounded by `|monster|^{ℵ_0}`.
- The product family becomes the product over types over a parameter
  set of size `|monster|`.
- The lower bound is attained when the theory has at least one type
  with a non-trivial automorphism class indexed by `|monster|`.

This structural alignment is the strongest evidence that the candidate
pattern is **uniform across branches** rather than P^1-specific.

## Status

This is a **proof sketch**, not a proof. Specifically, the upper bound
on `|F̂r_k|` for general fields, and the precise dependence of the
condensed π_1 quotient on the exact index family, would each need to be
verified for each scheme class. We have not done that verification.

The argument is **plausible and structural**. It should be either
provable as a theorem or refutable by an explicit counterexample
within the existing condensed mathematics machinery.

## Phase 4 question (sharpened)

> Is there a smooth finite-type scheme `X` over an infinite field `k`
> for which `|π_1^{cond}(X_k)(*)| ≠ 2^|k|`? Both directions are interesting:
>
> - If `|π_1^{cond}(X_k)(*)| > 2^|k|`: the envelope is wrong (and
>   we have not seen any case where this happens).
> - If `|π_1^{cond}(X_k)(*)| < 2^|k|`: the lower bound is not always
>   attained, refining the candidate pattern from "envelope" to
>   "envelope sometimes attained".

The simplest place to look for the second case is `X = Spec(k)` with
trivial `π_1^cond`, or `X` with no closed points outside the algebraic
closure.
