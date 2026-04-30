from axiom_explorer.seeds import SEEDS, all_codes, binary_combinations


def test_four_seeds():
    assert set(SEEDS.keys()) == {"A1", "A2", "A3", "A4"}


def test_all_codes_order():
    assert all_codes() == ["A1", "A2", "A3", "A4"]


def test_binary_combinations_count():
    pairs = binary_combinations()
    assert len(pairs) == 6
    assert ("A1", "A2") in pairs
    assert ("A3", "A4") in pairs
    seen = set()
    for a, b in pairs:
        assert a < b
        assert (a, b) not in seen
        seen.add((a, b))


def test_each_seed_has_terms_and_authors():
    for code, seed in SEEDS.items():
        assert seed.primary_terms, f"{code} missing primary terms"
        assert seed.related_terms, f"{code} missing related terms"
        assert seed.key_authors, f"{code} missing key authors"
        assert seed.branch
        assert seed.name


def test_scholze_appears_in_both_a2_and_a3():
    """Sanity: Scholze should be a key author of both Condensed and Perfectoid."""
    assert "Scholze" in SEEDS["A2"].key_authors
    assert "Scholze" in SEEDS["A3"].key_authors
