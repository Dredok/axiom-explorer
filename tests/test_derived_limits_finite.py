"""Tests for the finite-case sanity check of Bergfalk-LH §2 definitions."""

from axiom_explorer.compute.derived_limits_finite import (
    embedding_test_finite,
    lim_n_finite_A_kappa_lambda,
    run_all,
)


def test_finite_kappa_implies_vanishing():
    out = lim_n_finite_A_kappa_lambda(kappa=2, lam=3, n=1)
    assert out["lim_n_vanishes"] is True


def test_finite_lambda_implies_vanishing():
    out = lim_n_finite_A_kappa_lambda(kappa=5, lam=1, n=2)
    assert out["lim_n_vanishes"] is True


def test_embedding_basic():
    out = embedding_test_finite(2, 2, 3, 3, 1)
    assert out["embedding_consistent"] is True
    assert out["|n-coh family on (k,l)|"] <= out["|n-coh family on (m,n)|"]


def test_embedding_rejects_bad_hypothesis():
    out = embedding_test_finite(5, 5, 3, 3, 1)
    assert "fails" in out["verdict"]


def test_run_all_consistent():
    out = run_all()
    assert out["theorem_2_10_1_finite_vanishing"]["all_vanish"] is True
    assert out["theorem_2_10_4_embedding"]["all_consistent"] is True
