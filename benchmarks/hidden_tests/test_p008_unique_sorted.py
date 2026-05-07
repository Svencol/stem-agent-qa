from benchmarks.problems.p008_unique_sorted import unique_sorted


def test_sorted_values():
    assert unique_sorted([3, 1, 2]) == [1, 2, 3]


def test_removes_duplicates():
    assert unique_sorted([3, 1, 3, 2]) == [1, 2, 3]
