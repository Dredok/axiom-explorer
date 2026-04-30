"""Tests that don't hit the network."""

from axiom_explorer.arxiv_search import _build_search_query


def test_build_query_and():
    q = _build_search_query(["univalence", "condensed mathematics"], operator="AND")
    assert q == 'all:"univalence" AND all:"condensed mathematics"'


def test_build_query_or():
    q = _build_search_query(["a", "b", "c"], operator="OR")
    assert q == 'all:"a" OR all:"b" OR all:"c"'
