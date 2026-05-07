from benchmarks.problems.p011_clamp import clamp


def test_inside_range():
    assert clamp(5, 1, 10) == 5


def test_above_upper_bound():
    assert clamp(11, 0, 10) == 10
