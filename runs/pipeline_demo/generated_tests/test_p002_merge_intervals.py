import pytest
from benchmarks.problems.p002_merge_intervals import merge_intervals

def test_merge_intervals():
    # Test case with overlapping intervals
    assert merge_intervals([(1, 3), (2, 4), (5, 7), (6, 8)]) == [(1, 4), (5, 8)]
    
    # Test case with adjacent intervals
    assert merge_intervals([(1, 3), (3, 5)]) == [(1, 5)]
    
    # Test case with non-overlapping intervals
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]
    
    # Test case with fully nested intervals
    assert merge_intervals([(1, 5), (2, 3), (4, 6)]) == [(1, 6)]
    
    # Test case with single interval
    assert merge_intervals([(1, 2)]) == [(1, 2)]
    
    # Test case with empty list
    assert merge_intervals([]) == []
    
    # Test case with intervals that are the same
    assert merge_intervals([(1, 2), (1, 2), (1, 2)]) == [(1, 2)]
    
    # Test case with multiple overlapping intervals
    assert merge_intervals([(1, 4), (2, 3), (5, 6), (7, 8), (6, 7)]) == [(1, 4), (5, 8)]

if __name__ == "__main__":
    pytest.main()
