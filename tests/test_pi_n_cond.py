"""Tests for the higher π_n^{cond} envelope predictions."""

from axiom_explorer.compute.condensed_pi1_cardinality import BETH_2, CONTINUUM
from axiom_explorer.compute.pi_n_cond import (
    PREDICTIONS,
    all_predictions,
    envelope_check,
    k3_n2_question,
)


def test_predictions_cover_n1_and_n2():
    ns = {p.n for p in PREDICTIONS}
    assert 1 in ns
    assert 2 in ns


def test_envelope_field_C_is_beth_2():
    for p in PREDICTIONS:
        if p.field == "C":
            assert p.predicted_envelope == BETH_2


def test_envelope_field_Q_is_c():
    for p in PREDICTIONS:
        if p.field == "Q":
            assert p.predicted_envelope == CONTINUUM


def test_k3_spotlight_question_is_well_formed():
    out = k3_n2_question()
    assert out["scheme"].startswith("K3")
    assert out["n"] == 2
    assert "open" in out["natural_question"].lower() or "open" in out["phase_5_relevance"].lower()


def test_each_envelope_check_has_claim():
    for p in PREDICTIONS:
        out = envelope_check(p)
        assert out["claim"]
        assert out["falsifiable_by"]


def test_all_predictions_serialise():
    rows = all_predictions()
    assert all("predicted_envelope_str" in r for r in rows)
