from benchmarks.problems.p009_get_middle import get_middle


def test_odd_length():
    assert get_middle([1, 2, 3]) == 2


def test_even_length_left_middle():
    assert get_middle([1, 2, 3, 4]) == 2
