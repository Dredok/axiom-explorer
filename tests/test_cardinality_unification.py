"""Tests for the cross-branch cardinality-envelope tracker."""

from axiom_explorer.compute.cardinality_unification import (
    GEOMETRIC,
    MODEL_THEORETIC,
    SET_THEORETIC,
    all_envelope_checks,
    falsifying_witnesses,
    unification_report,
)


def test_no_falsifying_witnesses():
    """The candidate pattern survives every attestation we recorded."""
    assert falsifying_witnesses() == []


def test_three_branches_attested():
    assert len(GEOMETRIC) >= 2
    assert len(MODEL_THEORETIC) >= 2
    assert len(SET_THEORETIC) >= 2


def test_unification_report_consistent():
    r = unification_report()
    assert r["all_consistent"] is True
    assert r["attestations_total"] == len(all_envelope_checks())
