"""Unified cardinality-envelope tracker across geometric, model-theoretic,
and set-theoretic instances of the same condensed classifying-anima
construction.

References:
- Haine-Holzschuh-Lara-Mair-Martini-Wolf, *The condensed homotopy type of
  a scheme*, arXiv:2510.07443 (Oct 2025): geometric side.
- Haine, *Classifying anima of condensed ∞-categories of points*,
  arXiv:2602.21330 (Feb 2026): unifies geometric and model-theoretic
  sides via condensed classifying anima.
- Bergfalk-Lambie-Hanson-Šaroch, *Whitehead's problem and condensed
  mathematics*, arXiv:2312.09122: condensed Whitehead via forcing-theoretic
  systems of names.
- Bannister-Basak, *Condensed Sets and the Solovay Model*,
  arXiv:2602.09283 (Feb 2026): geometric morphism from Solovay topos to
  κ-pyknotic, forcing-theoretic proof of the condensed Whitehead.

Candidate pattern (axiom-explorer C-A2A3-2 dossier):

  All three sides of the unified condensed picture obey a cardinality
  envelope of the form `2^kappa`, where `kappa` is the relevant base
  cardinal:
    - geometric: kappa = |k|, k a base field.
    - model-theoretic: kappa = |monster| of a complete theory T.
    - set-theoretic: kappa = |R|, the cardinality of the reals.

This module gathers attestations from each side, presents the unified
picture, and flags where a falsifying computation would land.
"""

from __future__ import annotations

from dataclasses import dataclass

from axiom_explorer.compute.condensed_pi1_cardinality import (
    ALEPH_0,
    BETH_2,
    CONTINUUM,
    Cardinal,
)


@dataclass(frozen=True)
class Attestation:
    side: str
    invariant: str
    base_cardinal: Cardinal
    invariant_size: Cardinal
    source: str


GEOMETRIC: list[Attestation] = [
    Attestation(
        side="geometric",
        invariant="|π_1^{cond}(P^1_C)|",
        base_cardinal=CONTINUUM,
        invariant_size=BETH_2,
        source="Haine et al. arXiv:2510.07443, Remark 7.14",
    ),
    Attestation(
        side="geometric",
        invariant="|π_1^{cond}(P^1_Q)| upper bound",
        base_cardinal=ALEPH_0,
        invariant_size=CONTINUUM,
        source="Haine et al. arXiv:2510.07443, Remark 7.14",
    ),
]

MODEL_THEORETIC: list[Attestation] = [
    Attestation(
        side="model-theoretic",
        invariant="|Gal_L(DLO)|",
        base_cardinal=CONTINUUM,
        invariant_size=Cardinal(0),  # trivial
        source="DLO is omega-categorical, simple => Lascar trivial",
    ),
    Attestation(
        side="model-theoretic",
        invariant="|Gal_L(ACF_0)|",
        base_cardinal=CONTINUUM,
        invariant_size=Cardinal(0),
        source="ACF_0 is omega-stable, simple => Lascar trivial",
    ),
    Attestation(
        side="model-theoretic",
        invariant="|Gal_L(wild T, |T|=c)|",
        base_cardinal=CONTINUUM,
        invariant_size=BETH_2,  # can attain 2^c
        source="Casanovas, Simple Theories, hyperimaginaries chapter",
    ),
]

SET_THEORETIC: list[Attestation] = [
    Attestation(
        side="set-theoretic",
        invariant="Whitehead resolution in condensed Ab",
        base_cardinal=CONTINUUM,
        invariant_size=CONTINUUM,  # the relevant cardinal is |R|
        source="Clausen-Scholze + Bergfalk-LH-Saroch arXiv:2312.09122",
    ),
    Attestation(
        side="set-theoretic",
        invariant="Solovay topos -> kappa-pyknotic",
        base_cardinal=CONTINUUM,
        invariant_size=CONTINUUM,
        source="Bannister-Basak arXiv:2602.09283",
    ),
]


def envelope_check(att: Attestation) -> dict:
    """Test that an attested invariant size respects the predicted envelope
    `<= 2^kappa` (i.e. the next beth level above kappa)."""
    predicted_envelope = Cardinal(att.base_cardinal.tower_height + 1)
    respects = att.invariant_size <= predicted_envelope
    return {
        "side": att.side,
        "invariant": att.invariant,
        "base_cardinal": str(att.base_cardinal),
        "invariant_size": str(att.invariant_size),
        "predicted_envelope": str(predicted_envelope),
        "respects_envelope": respects,
        "source": att.source,
    }


def all_envelope_checks() -> list[dict]:
    return [envelope_check(a) for a in GEOMETRIC + MODEL_THEORETIC + SET_THEORETIC]


def falsifying_witnesses() -> list[dict]:
    """Find any attestation that EXCEEDS the predicted envelope."""
    return [c for c in all_envelope_checks() if not c["respects_envelope"]]


def unification_report() -> dict:
    return {
        "candidate_pattern": (
            "For invariants arising as the underlying group at section level "
            "of the condensed classifying anima of a spectral ∞-topos, the "
            "cardinality envelope is `2^kappa` where kappa is the cardinality "
            "of the underlying point set."
        ),
        "unifying_construction": (
            "Haine arXiv:2602.21330 Theorem 0.3: for a spectral ∞-topos 𝒳, "
            "B Pt^coh(𝒳) ≃ B Pt(𝒳) (induced equivalence on classifying "
            "anima). The geometric and model-theoretic sides are special "
            "cases."
        ),
        "attestations_total": len(GEOMETRIC) + len(MODEL_THEORETIC) + len(SET_THEORETIC),
        "geometric_count": len(GEOMETRIC),
        "model_theoretic_count": len(MODEL_THEORETIC),
        "set_theoretic_count": len(SET_THEORETIC),
        "envelope_checks": all_envelope_checks(),
        "falsifying_witnesses": falsifying_witnesses(),
        "all_consistent": len(falsifying_witnesses()) == 0,
    }
