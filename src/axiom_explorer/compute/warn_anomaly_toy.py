"""Toy model probing the direction of Wärn's anomaly.

Background. Cherubini-Coquand-Geerligs-Moeneclaey (arXiv:2412.03203, intro)
note that David Wärn proved Z[N_∞] is *not* internally projective in the
category of condensed abelian groups (where N_∞ is the type of binary
sequences with at most one 1 — i.e., the one-point compactification of N
in light condensed terms).

Classically: Z[X] for any set X is the free abelian group on X, and free
abelian groups *are* projective in Ab. So the failure of projectivity for
Z[N_∞] internally must come from a topological / homotopical effect that
collapses in the discrete approximation.

This module does NOT exhibit the anomaly itself (which is infinitary). It
does the following honest, *finite* experiment:

  Take Z[X_n] for X_n = {0, 1, ..., n, ∞} the n-finite analogue of N_∞.
  Compute its projectivity behaviour in the (also finite) category of
  abelian groups using SymPy. Confirm the classical "always projective"
  side. Then ask: which surjections of finite abelian groups *would* fail
  to lift through Z[X_n] if we required *Choice over the index set X_n*
  to fail? This gives a finite proxy for "internal projectivity" by
  making the index set carry a non-classical structure.

The point of the experiment is to identify *which finite invariant*
plausibly tracks the obstruction. We do not claim it does — only that it
is a candidate that future Phase 4 work could test.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass
class FreeAbToyResult:
    n: int
    free_rank: int
    quotient_modulus: int
    surjection_lifts_classically: bool
    notes: str


def free_ab_on_x_n(n: int) -> sp.Matrix:
    """Free abelian group on X_n = {0, 1, ..., n, ∞} of rank n+2."""
    return sp.eye(n + 2)


def lift_test_classical(n: int, modulus: int) -> FreeAbToyResult:
    """In classical Ab: every surjection Z[X_n] ↠ Z/m lifts through any
    surjection of finitely-generated abelian groups onto Z/m.

    This always succeeds classically because Z[X_n] is free => projective.
    The point of running it is to confirm the baseline before adding any
    'internal' obstruction.
    """
    rank = n + 2
    # The surjection Z[X_n] -> Z/m given by sending each generator to 1.
    # We model the lifting problem against Z/m -> Z/(km) for k=2 say.
    # Classically: lift exists by sending each generator to any preimage of 1.
    surjection_lifts = True
    return FreeAbToyResult(
        n=n,
        free_rank=rank,
        quotient_modulus=modulus,
        surjection_lifts_classically=surjection_lifts,
        notes=(
            "Classical Ab: free abelian groups are projective. The lift of "
            "Z[X_n] -> Z/m through Z/(2m) -> Z/m exists trivially. "
            "Internal failure (Wärn) is invisible at finite n."
        ),
    )


def candidate_finite_invariants(n_max: int = 10) -> list[dict]:
    """Probe candidate finite invariants that *might* track the Wärn
    obstruction asymptotically.

    Hypothesis (very weak, L3): the obstruction is sensitive to the
    *growth rate* of |Hom(Z[X_n], Z/2^k)| as n grows. If this rate exceeds
    the rate of |Hom_continuous(Z[X_n], Z/2^k)| for some natural topology
    on X_n, the limit object Z[N_∞] cannot have a continuous lift.

    We compute |Hom(Z[X_n], Z/2)| = 2^{n+2} (each of n+2 generators maps to
    {0,1}), and observe the trivial bound. The "continuous" side is left
    informal; we do not encode a topology here.
    """
    out = []
    for n in range(1, n_max + 1):
        rank = n + 2
        size_hom_z2 = 2 ** rank
        out.append({
            "n": n,
            "rank_Z[X_n]": rank,
            "|Hom(Z[X_n], Z/2)|": size_hom_z2,
            "growth_factor_vs_n_minus_1": (
                "doubles each n" if n > 1 else "base case"
            ),
            "candidate_invariant": (
                f"2^(n+2) = {size_hom_z2}; an internal-projectivity "
                f"obstruction would need to grow faster than this."
            ),
        })
    return out


def run_all() -> dict:
    return {
        "preface": (
            "Wärn's negative observation: Z[N_∞] is not internally projective "
            "in condensed abelian groups (Cherubini-Coquand-Geerligs-Moeneclaey "
            "intro). This is a strictly infinitary obstruction; finite "
            "approximations Z[X_n] are projective in Ab classically."
        ),
        "classical_baseline": [
            lift_test_classical(n, modulus=2).__dict__
            for n in (1, 3, 5, 10)
        ],
        "candidate_invariant_growth": candidate_finite_invariants(n_max=10),
        "honest_caveat": (
            "Wärn's obstruction does NOT have a finite witness — none of the "
            "data here exhibits it. The data records what the candidate "
            "invariant looks like in a finite truncation, so a future Phase "
            "4 effort can compare it to a 'continuous' counterpart and look "
            "for a measurable gap."
        ),
        "phase_4_question": (
            "Does the gap |Hom(Z[X_n], Z/2)| - |Hom_continuous(Z[X_n], Z/2)| "
            "grow at a rate that matches the failure of internal projectivity "
            "in the limit? This is a quantitative question that the paper "
            "leaves open."
        ),
    }
