"""Cardinality envelope for higher condensed homotopy groups π_n^{cond}.

Extension of the C-A2A3-2 candidate to the higher π_n's, n ≥ 2.

Reasoning:
- Π_∞^{cond}(X) ≃ B Pt^{coh}(X_ét) (Haine et al. arXiv:2510.07443).
- π_n^{cond}(X, x̄) is the n-th homotopy group of the condensed anima
  B Pt^{coh}(X_ét) at the basepoint x̄.
- Each π_n is the underlying group of section Hom into a (possibly
  non-discrete) loop space n-fold iterated.
- All these groups are subquotients of profinite groups indexed by
  the underlying set of X (closed points / Galois of generic), whose
  cardinality is bounded by |k|^{ℵ_0} = 2^|k| for infinite k.

So the candidate:

    |π_n^{cond}(X_k, x̄)(*)|  ≤  2^|k|  for all n ≥ 1.

The bound is **attained for n=1** when X has nontrivial étale H_1
(by the paper's own argument). For n ≥ 2, attainment depends on the
higher étale homotopy of X. Open: characterise exactly when each
π_n attains the bound.

This module also tracks an **expected sequence** of cardinalities for
some standard examples, making predictions falsifiable.
"""

from __future__ import annotations

from dataclasses import dataclass

from axiom_explorer.compute.condensed_pi1_cardinality import (
    BETH_2,
    CONTINUUM,
    Cardinal,
)


@dataclass(frozen=True)
class PiNPrediction:
    scheme: str
    field: str
    n: int
    classical_pi_n_et: str
    predicted_envelope: Cardinal
    note: str


# Predictions for some standard schemes.
# We use the rule: |π_n^{cond}(X_k)| <= 2^|k| for all n >= 1.

PREDICTIONS: list[PiNPrediction] = [
    # P^1 over C: π_1^et = 1, π_n^et = 0 for n >= 2 (in char 0)
    # Paper attests π_1^cond(P^1_C) = 2^c. Higher π_n^cond ≤ 2^c by our bound.
    PiNPrediction(
        scheme="P^1",
        field="C",
        n=1,
        classical_pi_n_et="trivial",
        predicted_envelope=BETH_2,
        note="Attested as 2^c by Haine et al. Remark 7.14.",
    ),
    PiNPrediction(
        scheme="P^1",
        field="C",
        n=2,
        classical_pi_n_et="trivial",
        predicted_envelope=BETH_2,
        note=(
            "Open: π_2^cond(P^1_C) is bounded by 2^c by our envelope. "
            "Probably trivial since classical pi_2^et trivial; the "
            "condensed correction would only inject extra cardinality if "
            "the higher étale homotopy at section level introduced new "
            "torsion indexed by C, which is not expected for proper "
            "smooth varieties. Best guess: trivial or very small."
        ),
    ),
    # P^1 over Q: bounded by 2^aleph_0 = c
    PiNPrediction(
        scheme="P^1",
        field="Q",
        n=1,
        classical_pi_n_et="profinite of countable rank",
        predicted_envelope=CONTINUUM,
        note="Attested as ≤ c by Haine et al. Remark 7.14.",
    ),
    PiNPrediction(
        scheme="P^1",
        field="Q",
        n=2,
        classical_pi_n_et="trivial",
        predicted_envelope=CONTINUUM,
        note="Open. Same reasoning as P^1_C, n=2 case.",
    ),
    # E (elliptic curve) over C: π_1^et = Ẑ², π_n^et = 0 for n >= 2.
    PiNPrediction(
        scheme="E",
        field="C",
        n=1,
        classical_pi_n_et="Ẑ × Ẑ",
        predicted_envelope=BETH_2,
        note="Open. Bound: 2^c. Attainment expected because E has H_1.",
    ),
    PiNPrediction(
        scheme="E",
        field="C",
        n=2,
        classical_pi_n_et="trivial",
        predicted_envelope=BETH_2,
        note="Open. Bound: 2^c.",
    ),
    # K3 surface over C
    PiNPrediction(
        scheme="K3",
        field="C",
        n=1,
        classical_pi_n_et="trivial",
        predicted_envelope=BETH_2,
        note="Open. Bound: 2^c. May be trivial like P^1.",
    ),
    PiNPrediction(
        scheme="K3",
        field="C",
        n=2,
        classical_pi_n_et="non-trivial (H_2 of rank 22)",
        predicted_envelope=BETH_2,
        note=(
            "**Most interesting case**. K3 has rank-22 H_2; the condensed "
            "lift may capture something here. Bound: 2^c. Whether "
            "attained is open; this is a genuine prediction-target for "
            "Phase 5."
        ),
    ),
]


def all_predictions() -> list[dict]:
    return [p.__dict__ | {"predicted_envelope_str": str(p.predicted_envelope)} for p in PREDICTIONS]


def k3_n2_question() -> dict:
    """Spotlight K3 surface n=2 as the most interesting test case."""
    return {
        "scheme": "K3 surface over C",
        "n": 2,
        "classical_etale": "non-trivial; H_2(K3_C, Z_l) = Z_l^22",
        "candidate_envelope": str(BETH_2),
        "natural_question": (
            "Does the condensed enhancement of the K3 étale homotopy type at n=2 "
            "see additional cardinality beyond the rank-22 of classical H_2? "
            "Specifically, does π_2^cond(K3_C)(*) attain 2^c, or is it bounded "
            "by ((Z_l)^22)^c = 2^c structurally but 'detected' only at countable "
            "rank?"
        ),
        "phase_5_relevance": (
            "K3 is the cleanest non-trivial smooth proper case after P^1. The "
            "answer would tell us whether the condensed structure at n>=2 carries "
            "new cardinality information beyond the étale rank, or just amplifies "
            "what's already there. This question is genuinely open in our reading."
        ),
    }


def envelope_check(p: PiNPrediction) -> dict:
    """We can't test attainment here (no direct π_n^cond computation); we
    record the envelope claim so future computations can falsify it."""
    return {
        "scheme": p.scheme,
        "field": p.field,
        "n": p.n,
        "predicted_envelope": str(p.predicted_envelope),
        "claim": f"|π_{p.n}^cond({p.scheme}_{p.field})(*)| <= {p.predicted_envelope}",
        "falsifiable_by": "any direct computation exceeding the envelope",
    }


def run_all() -> dict:
    return {
        "candidate": (
            "|π_n^{cond}(X_k, x̄)(*)| ≤ 2^|k| for all n ≥ 1, X smooth qcqs over infinite k. "
            "Inherits from C-A2A3-2 by structural argument: each π_n is a subquotient "
            "of profinite groups indexed by |X| ≤ |k|^{aleph_0} = 2^|k|."
        ),
        "predictions": all_predictions(),
        "spotlight_k3_n2": k3_n2_question(),
        "envelope_checks": [envelope_check(p) for p in PREDICTIONS],
        "honesty": (
            "All n >= 2 predictions are L3 (speculative). Haine et al. only "
            "attest π_0 and π_1 explicitly. The maybe-most-illuminating test "
            "case (K3 surface, n=2) is genuinely open in our reading."
        ),
    }
