from benchmarks.problems.p002_merge_intervals import merge_intervals

def test_merge_intervals_normal_cases():
    assert merge_intervals([(1, 3), (2, 4), (5, 7)]) == [(1, 4), (5, 7)]
    assert merge_intervals([(1, 4), (2, 3), (5, 6)]) == [(1, 4), (5, 6)]
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]

def test_merge_intervals_edge_cases():
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 2)]) == [(1, 2)]
    assert merge_intervals([(1, 3), (3, 3), (2, 4)]) == [(1, 4)]
    assert merge_intervals([(1, 5), (2, 3), (4, 6)]) == [(1, 6)]

def test_merge_intervals_stability():
    intervals = [(1, 3), (2, 4), (5, 7)]
    original_intervals = intervals.copy()
    result = merge_intervals(intervals)
    assert result == [(1, 4), (5, 7)]
    assert intervals == original_intervals  # Check that the original list is unchanged

def test_merge_intervals_with_duplicates():
    assert merge_intervals([(1, 3), (2, 3), (3, 5), (5, 5)]) == [(1, 5)]
