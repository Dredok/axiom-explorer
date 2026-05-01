"""Tests for the finite-model sanity check of Synthetic Stone Duality axioms."""

import pytest

z3 = pytest.importorskip("z3")

from axiom_explorer.compute.stone_duality_finite_model import (  # noqa: E402
    axiom_independence_check,
    consequence_finite_LLPO,
    consequence_finite_markov,
)


def test_axiom2_finite_no_violations():
    """Axiom 2 (surj iff inj on pullback) holds for all finite n=3,4 functions."""
    for n in (3, 4):
        out = axiom_independence_check(n=n)
        a2 = out["checks"]["axiom2_finite"]
        assert a2["violations"] == [], (
            f"Axiom 2 violation found at n={n}: {a2['violations']}"
        )


def test_LLPO_holds_in_finite_N_inf():
    for n in (3, 5):
        out = consequence_finite_LLPO(n=n)
        assert out["LLPO_holds_finitely"] is True
        assert out["counterexamples_to_LLPO_in_finite_N_inf"] == []


def test_markov_holds_in_finite_case():
    for n in (3, 5):
        out = consequence_finite_markov(n=n)
        assert out["markov_holds_finitely"] is True
        assert out["markov_failures_in_finite_case"] == []
