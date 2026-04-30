from axiom_explorer.phases.phase0_bibliometric import _classify, _query_terms_for_pair, _slug


def test_classify_thresholds():
    assert _classify(0) == "virgin"
    assert _classify(4) == "virgin"
    assert _classify(5) == "sparse"
    assert _classify(29) == "sparse"
    assert _classify(30) == "warm"
    assert _classify(99) == "warm"
    assert _classify(100) == "saturated"


def test_slug_basic():
    assert _slug("Hello World") == "hello-world"
    assert _slug('"quoted phrase"') == "quoted-phrase"
    assert _slug("CD(K,N)") == "cdkn"


def test_query_fanout_nonempty():
    qs = _query_terms_for_pair("A1", "A2")
    assert len(qs) >= 1
    # All queries are 2-element AND-pairs
    assert all(len(q) == 2 for q in qs)
