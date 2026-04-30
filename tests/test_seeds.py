from axiom_explorer.seeds import SEEDS, all_codes, binary_combinations


def test_four_seeds():
    assert set(SEEDS.keys()) == {"A1", "A2", "A3", "A4"}


def test_all_codes_order():
    codes = all_codes()
    assert codes == ["A1", "A2", "A3", "A4"]


def test_binary_combinations_count():
    pairs = binary_combinations()
    # C(4, 2) = 6
    assert len(pairs) == 6
    assert ("A1", "A2") in pairs
    assert ("A3", "A4") in pairs
    # No duplicates / no reversals
    seen = set()
    for a, b in pairs:
        assert a < b
        assert (a, b) not in seen
        seen.add((a, b))


def test_each_seed_has_primary_terms():
    for code, seed in SEEDS.items():
        assert len(seed.primary_terms) >= 1, f"{code} missing primary terms"
        assert seed.branch
        assert seed.name
