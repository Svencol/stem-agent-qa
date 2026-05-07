from benchmarks.problems.p007_safe_divide import safe_divide


def test_normal_division():
    assert safe_divide(10, 2) == 5.0


def test_divide_by_zero():
    assert safe_divide(10, 0) is None
