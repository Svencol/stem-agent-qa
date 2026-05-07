import pytest
from benchmarks.problems.p004_find_max import find_max

def test_find_max():
    # Test with positive integers
    assert find_max([1, 5, 2]) == 5
    
    # Test with negative integers
    assert find_max([-10, -3, -7]) == -3
    
    # Test with a mix of positive and negative integers
    assert find_max([-1, 0, 1]) == 1
    
    # Test with all negative integers
    assert find_max([-2, -5, -1]) == -1
    
    # Test with a single element
    assert find_max([42]) == 42
    
    # Test with large integers
    assert find_max([1000000, 999999, 1000001]) == 1000001
