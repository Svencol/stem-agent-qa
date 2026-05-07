from benchmarks.problems.p004_find_max import find_max


def test_positive():
    assert find_max([1, 5, 2]) == 5


def test_all_negative():
    assert find_max([-10, -3, -7]) == -3
