from benchmarks.problems.p012_remove_none import remove_none


def test_removes_none_values():
    assert remove_none([1, None, 2, None]) == [1, 2]


def test_does_not_mutate_input():
    values = [1, None, 2]
    result = remove_none(values)

    assert result == [1, 2]
    assert values == [1, None, 2]
