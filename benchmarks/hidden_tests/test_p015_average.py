from benchmarks.problems.p015_average import average


def test_average_non_empty():
    assert average([1, 2, 3]) == 2.0


def test_average_empty_list():
    assert average([]) is None
