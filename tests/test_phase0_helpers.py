from axiom_explorer.phases.phase0_bibliometric import _classify, _slug


def test_classify_thresholds_unbridged():
    assert _classify(0, has_community_bridge=False) == "virgin"
    assert _classify(4, has_community_bridge=False) == "virgin"
    assert _classify(5, has_community_bridge=False) == "sparse"
    assert _classify(29, has_community_bridge=False) == "sparse"
    assert _classify(30, has_community_bridge=False) == "warm"
    assert _classify(99, has_community_bridge=False) == "warm"
    assert _classify(100, has_community_bridge=False) == "saturated"


def test_classify_bridge_promotes_low_counts():
    assert _classify(0, has_community_bridge=True) == "frontier-bridged"
    assert _classify(4, has_community_bridge=True) == "frontier-bridged"
    assert _classify(5, has_community_bridge=True) == "warm-bridged"
    assert _classify(29, has_community_bridge=True) == "warm-bridged"
    # Bridge does not downgrade saturated/warm classifications.
    assert _classify(30, has_community_bridge=True) == "warm"
    assert _classify(100, has_community_bridge=True) == "saturated"


def test_slug_basic():
    assert _slug("Hello World") == "hello-world"
    assert _slug('"quoted phrase"') == "quoted-phrase"
    assert _slug("CD(K,N)") == "cdkn"
