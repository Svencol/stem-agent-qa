from benchmarks.problems.p002_merge_intervals import merge_intervals

def test_merge_intervals_normal_cases():
    assert merge_intervals([(1, 3), (2, 4), (5, 7)]) == [(1, 4), (5, 7)]
    assert merge_intervals([(1, 4), (2, 3), (5, 6)]) == [(1, 4), (5, 6)]
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]

def test_merge_intervals_edge_cases():
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 1)]) == [(1, 1)]
    assert merge_intervals([(1, 2), (2, 3)]) == [(1, 3)]
    assert merge_intervals([(1, 5), (5, 10)]) == [(1, 10)]

def test_merge_intervals_side_effects():
    intervals = [(1, 3), (2, 4)]
    original_intervals = intervals.copy()
    result = merge_intervals(intervals)
    assert intervals == original_intervals
    assert result == [(1, 4)]
