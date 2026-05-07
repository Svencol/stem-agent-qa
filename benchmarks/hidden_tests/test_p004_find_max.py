from benchmarks.problems.p004_find_max import find_max


def test_positive_values():
    assert find_max([1, 5, 2]) == 5


def test_all_negative_values():
    assert find_max([-10, -3, -7]) == -3
