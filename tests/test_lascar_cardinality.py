"""Tests for Lascar/condensed cardinality cross-check."""

from axiom_explorer.compute.lascar_cardinality import (
    LASCAR_TEST_CASES,
    check_pattern_against_lascar,
    cross_pattern_summary,
)


def test_no_disagreements_with_classical_lascar():
    """Every classical Lascar bound we listed must respect the predicted envelope."""
    out = check_pattern_against_lascar()
    assert out["disagreements"] == [], (
        f"Lascar bound exceeds predicted envelope in {out['disagreements']}"
    )
    assert len(out["agreements"]) == len(LASCAR_TEST_CASES)


def test_cross_pattern_summary_has_both_sides():
    s = cross_pattern_summary()
    assert s["geometric_attestations"]
    assert s["model_theoretic_attestations"]
    assert s["claim"]
