import pytest
from benchmarks.problems.p008_unique_sorted import unique_sorted

def test_unique_sorted():
    # Test with duplicates
    assert unique_sorted([3, 1, 3, 2]) == [1, 2, 3]
    assert unique_sorted([5, 5, 5, 5]) == [5]
    assert unique_sorted([1, 2, 2, 3, 1]) == [1, 2, 3]
    
    # Test with already sorted unique values
    assert unique_sorted([1, 2, 3]) == [1, 2, 3]
    
    # Test with an empty list
    assert unique_sorted([]) == []
    
    # Test with negative numbers
    assert unique_sorted([-1, -3, -2, -1]) == [-3, -2, -1]
    
    # Test with a mix of positive and negative numbers
    assert unique_sorted([-1, 0, 1, 0, -1]) == [-1, 0, 1]

    # Test with a large range of numbers
    assert unique_sorted(list(range(1000, 990, -1)) + list(range(995, 1005))) == list(range(990, 1005))
