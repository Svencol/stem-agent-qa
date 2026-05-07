from benchmarks.problems.p002_merge_intervals import merge_intervals
import pytest

def test_merge_intervals_normal_cases():
    assert merge_intervals([(1, 3), (2, 4)]) == [(1, 4)]
    assert merge_intervals([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]
    assert merge_intervals([(1, 5), (2, 3), (6, 8)]) == [(1, 5), (6, 8)]

def test_merge_intervals_edge_cases():
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 1)]) == [(1, 1)]
    assert merge_intervals([(1, 2), (2, 3)]) == [(1, 3)]
    assert merge_intervals([(1, 3), (3, 3)]) == [(1, 3)]

def test_merge_intervals_side_effects():
    intervals = [(1, 3), (2, 4)]
    original_intervals = intervals.copy()
    merge_intervals(intervals)
    assert intervals == original_intervals

def test_merge_intervals_with_duplicates():
    assert merge_intervals([(1, 3), (2, 3), (3, 5)]) == [(1, 5)]

def test_merge_intervals_boundary_conditions():
    assert merge_intervals([(1, 2), (2, 2), (2, 3)]) == [(1, 3)]
