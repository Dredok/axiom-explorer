"""Tests for the cardinality skeleton of the condensed π_1 candidate pattern."""

from axiom_explorer.compute.condensed_pi1_cardinality import (
    ALEPH_0,
    BETH_2,
    CONTINUUM,
    CandidatePatternBound,
    Cardinal,
    check_pattern_against_attested,
    kappa_of_field,
)


def test_cardinal_ordering():
    assert ALEPH_0 < CONTINUUM < BETH_2
    assert ALEPH_0 == Cardinal(0)
    assert CONTINUUM == Cardinal(1)


def test_kappa_of_field_known():
    assert kappa_of_field("C") == CONTINUUM
    assert kappa_of_field("Q") == ALEPH_0
    assert kappa_of_field("Cp") == CONTINUUM


def test_pattern_matches_attested_P1_C():
    pred = CandidatePatternBound("P^1", "C").predicted_bound()
    assert pred == BETH_2  # paper attests beth_2 for P^1_C


def test_pattern_matches_attested_P1_Q():
    pred = CandidatePatternBound("P^1", "Q").predicted_bound()
    assert pred == CONTINUUM  # paper attests c for P^1_Q


def test_no_disagreements_with_paper():
    out = check_pattern_against_attested()
    assert out["disagreements"] == []
    assert len(out["agreements"]) == 3
