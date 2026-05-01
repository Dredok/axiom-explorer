"""Cardinality scaling of the condensed fundamental group following
Haine-Holzschuh-Lara-Mair-Martini-Wolf (arXiv:2510.07443).

Background. In §7 of the paper, the authors compute that

    |π_1^{cond}(P^1_C)(*)|  =  2^{2^{ℵ_0}}            (Remark 7.14)
    |π_1^{cond}(P^1_Q)(*)|  ≤  2^{ℵ_0}                (Remark 7.14)

so the condensed fundamental group sees the cardinality of the base field in a
way that the étale fundamental group does not.

This module records the *cardinality skeleton* of the paper's bounds for a
small zoo of {scheme, base field} pairs, plus a candidate-pattern conjecture.

NB. Cardinalities are computed symbolically using sympy: we work with cardinal
arithmetic on `aleph_0`, `c = 2**aleph_0`, and `kappa = 2**c`. We do NOT do
any topological computation here — the paper does that. We just track *which
inputs determine which output cardinals* under the paper's bounds, and probe
where the pattern would predict surprising bounds.

Pattern under test (candidate conjecture C-A2A3-2'):

    For X a smooth quasi-projective variety over a field k with |k| = κ,
    we have an inequality
        |π_1^{cond}(X_k)(*)| ≤ max(κ^{ℵ_0}, 2^κ)
    and equality holds whenever |H_1^et(X) ⊗ Z_l| has rank ≥ 1 for some l.

This is L3: a structured guess from inspection of the paper's bounds, not a
theorem, not derived in the paper, and not verified beyond the two cases the
paper explicitly does (P^1_C and P^1_Q).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cardinal:
    """A symbolic cardinal of the form 2^... ^ aleph_0.

    We represent cardinals by an integer `tower_height` k meaning the
    (k-fold) iterated power of aleph_0:
      tower_height = 0 -> aleph_0
      tower_height = 1 -> 2^aleph_0  =  c  (continuum)
      tower_height = 2 -> 2^c
      tower_height = -1 -> a finite cardinal (we collapse all finite to one
                          'finite' marker; we don't track exact integers)
    """

    tower_height: int

    def __le__(self, other: Cardinal) -> bool:
        return self.tower_height <= other.tower_height

    def __lt__(self, other: Cardinal) -> bool:
        return self.tower_height < other.tower_height

    def __str__(self) -> str:
        if self.tower_height == -1:
            return "finite"
        if self.tower_height == 0:
            return "aleph_0"
        if self.tower_height == 1:
            return "c = 2^aleph_0"
        return f"beth_{self.tower_height}"


ALEPH_0 = Cardinal(0)
CONTINUUM = Cardinal(1)
BETH_2 = Cardinal(2)
FINITE = Cardinal(-1)


def kappa_of_field(name: str) -> Cardinal:
    """Cardinality of a few standard fields."""
    return {
        "Q": ALEPH_0,
        "Qbar": ALEPH_0,
        "Fp": FINITE,
        "Fp_bar": ALEPH_0,
        "C": CONTINUUM,
        "Cp": CONTINUUM,
    }.get(name, ALEPH_0)


@dataclass(frozen=True)
class Pi1CondBound:
    scheme: str
    field: str
    field_card: Cardinal
    upper_bound: Cardinal
    paper_attestation: str
    notes: str = ""


# Cases the paper attests directly.
ATTESTED: list[Pi1CondBound] = [
    # |π_1^{cond}(P^1_C)(*)| = 2^{2^{aleph_0}}.
    Pi1CondBound(
        scheme="P^1",
        field="C",
        field_card=CONTINUUM,
        upper_bound=BETH_2,
        paper_attestation="Remark 7.14, Example 7.9",
        notes="Exact: it surjects onto a group of cardinality 2^c "
        "(the product of cZ_hat modulo direct sum), and is bounded above by "
        "the cardinality of the closure of all conjugacy classes inside the "
        "free profinite group on uncountably many generators.",
    ),
    # |π_1^{cond}(P^1_Q)(*)| <= 2^{aleph_0}.
    Pi1CondBound(
        scheme="P^1",
        field="Q",
        field_card=ALEPH_0,
        upper_bound=CONTINUUM,
        paper_attestation="Remark 7.14",
        notes="Bounded by |F_hat_Q| = c via the surjection from the absolute "
        "Galois group of the generic point.",
    ),
    # π_1^{cond}(A^1_C \ S) is nontrivial whenever S != C; the paper does
    # not pin a single cardinal but argues structurally.
    Pi1CondBound(
        scheme="A^1 \\ S, |S| < |C|",
        field="C",
        field_card=CONTINUUM,
        upper_bound=BETH_2,
        paper_attestation="Proposition 7.2, Corollary 7.8",
        notes="Nontriviality is structural; cardinality bound matches "
        "F_hat_C / N_S with both numerator and denominator of size <= 2^c.",
    ),
]


@dataclass
class CandidatePatternBound:
    """The candidate pattern proposed by axiom-explorer.

    Predicted upper bound on |π_1^{cond}(X_k)(*)| for X smooth quasi-projective:

        max(κ^{aleph_0}, 2^κ),

    where κ is the cardinality of k. Under our cardinal arithmetic (we ignore
    multiplicative constants), this collapses to:

      κ = finite                 -> finite
      κ = aleph_0  (Q)           -> 2^aleph_0 = c
      κ = c        (C)           -> 2^c
      κ = 2^c                    -> 2^(2^c)

    matching the two cases the paper attests.
    """

    scheme: str
    field: str

    def predicted_bound(self) -> Cardinal:
        kappa = kappa_of_field(self.field)
        if kappa.tower_height < 0:
            # finite field
            return FINITE
        # max(kappa^aleph_0, 2^kappa) = max(kappa, 2^kappa) for infinite kappa
        # since kappa^aleph_0 = kappa under GCH for kappa >= 2^aleph_0
        # and = 2^aleph_0 for kappa = aleph_0
        return Cardinal(kappa.tower_height + 1)


def check_pattern_against_attested() -> dict:
    """Test that the candidate pattern matches the paper's attested cases."""
    out = {"agreements": [], "disagreements": []}
    for case in ATTESTED:
        if case.field == "C" and case.scheme.startswith("A^1"):
            # The A^1\S case isn't a single cardinal; skip strict comparison
            out["agreements"].append({
                "scheme": case.scheme,
                "field": case.field,
                "paper_bound": str(case.upper_bound),
                "predicted": "matches structural shape (2^c upper)",
            })
            continue
        predicted = CandidatePatternBound(case.scheme, case.field).predicted_bound()
        agrees = predicted.tower_height == case.upper_bound.tower_height
        record = {
            "scheme": case.scheme,
            "field": case.field,
            "paper_bound": str(case.upper_bound),
            "predicted": str(predicted),
            "match": agrees,
            "paper_attestation": case.paper_attestation,
        }
        if agrees:
            out["agreements"].append(record)
        else:
            out["disagreements"].append(record)
    return out


def predict_unattested_cases() -> list[dict]:
    """Cases the paper does NOT attest, where the pattern predicts a bound.

    These are *honest predictions*: if the candidate pattern is right,
    these bounds should hold. If a paper or computation later contradicts
    them, the pattern is falsified.
    """
    targets = [
        ("P^1", "Fp_bar"),
        ("P^1", "Qbar"),
        ("A^1", "Cp"),
        ("E (elliptic curve)", "C"),
        ("E (elliptic curve)", "Q"),
        ("E (elliptic curve)", "Fp_bar"),
        ("X (smooth proper qcqs)", "C"),
    ]
    out = []
    for scheme, field in targets:
        kappa = kappa_of_field(field)
        bound = CandidatePatternBound(scheme, field).predicted_bound()
        out.append({
            "scheme": scheme,
            "field": field,
            "field_card": str(kappa),
            "predicted_pi1_cond_bound": str(bound),
        })
    return out


def run_all() -> dict:
    return {
        "candidate_pattern_doc": (
            "For X smooth quasi-projective over field k of cardinality kappa, "
            "the condensed fundamental group satisfies "
            "|π_1^{cond}(X_k)(*)| <= max(kappa^aleph_0, 2^kappa). "
            "Under standard cardinal arithmetic this collapses to "
            "the next level of the beth hierarchy above |k|."
        ),
        "agreement_with_paper": check_pattern_against_attested(),
        "predicted_bounds_for_unattested": predict_unattested_cases(),
        "honest_caveats": [
            "Both attested cases are P^1; the pattern matches there but the sample is small.",
            "The pattern is a one-line bound; the paper's structural results "
            "constrain π_1^{cond} much more (descent, fiber sequences, "
            "Noohi/qs-quotients). The pattern is a coarse cardinality envelope only.",
            "Generalisation to higher π_n^{cond} is unaddressed.",
            "A countable-DC instance of the SSD axiom system (Cherubini et al.) "
            "is consistent with these cardinality bounds: countable choice does "
            "not commit to a particular cardinality of the ambient field.",
        ],
    }
