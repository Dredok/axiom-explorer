"""Phase 1 helper tests (no Mathlib clone required for these)."""

from axiom_explorer.phases.phase1_formal_state import (
    _scan_axioms,
    _scan_synthetic_zariski_open_questions,
)


def test_axioms_returns_list():
    # Test runs whether or not the artifact is present; if absent returns [].
    out = _scan_axioms()
    assert isinstance(out, list)
    for item in out:
        assert "name" in item and "body" in item


def test_open_questions_returns_list():
    out = _scan_synthetic_zariski_open_questions()
    assert isinstance(out, list)
    for item in out:
        assert "question" in item
