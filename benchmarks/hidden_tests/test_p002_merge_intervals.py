from benchmarks.problems.p002_merge_intervals import merge_intervals


def test_merge_overlapping():
    assert merge_intervals([(1, 3), (2, 5)]) == [(1, 5)]


def test_merge_touching_intervals():
    assert merge_intervals([(1, 3), (3, 5)]) == [(1, 5)]
