"""Tests for the Wärn anomaly toy model."""

from axiom_explorer.compute.warn_anomaly_toy import (
    candidate_finite_invariants,
    free_ab_on_x_n,
    lift_test_classical,
)


def test_free_ab_rank():
    M = free_ab_on_x_n(5)
    assert M.shape == (7, 7)


def test_classical_lift_always_succeeds():
    for n in (1, 3, 10):
        out = lift_test_classical(n, modulus=2)
        assert out.surjection_lifts_classically is True
        assert out.free_rank == n + 2


def test_candidate_invariant_doubles():
    out = candidate_finite_invariants(n_max=5)
    assert len(out) == 5
    sizes = [row["|Hom(Z[X_n], Z/2)|"] for row in out]
    # 2^(n+2) for n = 1..5 -> 8, 16, 32, 64, 128
    assert sizes == [8, 16, 32, 64, 128]
