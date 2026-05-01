"""Query-builder tests that don't hit the network."""

from axiom_explorer.arxiv_search import (
    _build_search_query,
    build_and_query,
    build_author_pair_query,
    build_grouped_and_query,
)


def test_build_and_query():
    q = build_and_query(["univalence", "condensed mathematics"])
    assert q == 'all:"univalence" AND all:"condensed mathematics"'


def test_legacy_alias_and():
    q = _build_search_query(["a", "b"])
    assert q == 'all:"a" AND all:"b"'


def test_build_grouped_and_query():
    q = build_grouped_and_query(["univalence", "HoTT"], ["condensed", "pyknotic"])
    assert q == '(all:"univalence" OR all:"HoTT") AND (all:"condensed" OR all:"pyknotic")'


def test_build_grouped_rejects_empty():
    import pytest

    with pytest.raises(ValueError):
        build_grouped_and_query([], ["b"])
    with pytest.raises(ValueError):
        build_grouped_and_query(["a"], [])


def test_build_author_pair_query_math_only_default():
    # math_only=True by default to filter namesake collisions with physics
    assert (
        build_author_pair_query("Scholze", "Lott")
        == 'au:"Scholze" AND au:"Lott" AND cat:math.*'
    )


def test_build_author_pair_query_no_math_filter():
    assert (
        build_author_pair_query("Scholze", "Lott", math_only=False)
        == 'au:"Scholze" AND au:"Lott"'
    )


def test_build_author_topic_query():
    from axiom_explorer.arxiv_search import build_author_topic_query
    q = build_author_topic_query("Haine", ["condensed", "perfectoid"])
    assert q == 'au:"Haine" AND (all:"condensed" OR all:"perfectoid") AND cat:math.*'


def test_build_author_topic_rejects_empty():
    import pytest

    from axiom_explorer.arxiv_search import build_author_topic_query
    with pytest.raises(ValueError):
        build_author_topic_query("Haine", [])
