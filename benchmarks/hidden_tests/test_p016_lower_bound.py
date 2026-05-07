from benchmarks.problems.p016_lower_bound import lower_bound


def test_exact_match():
    assert lower_bound([1, 3, 5, 7], 5) == 2


def test_between_values():
    assert lower_bound([1, 3, 5, 7], 4) == 2


def test_target_larger_than_all_values():
    assert lower_bound([1, 3, 5, 7], 8) == 4


def test_empty_list():
    assert lower_bound([], 10) == 0
