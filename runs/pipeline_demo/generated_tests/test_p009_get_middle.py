import pytest
from benchmarks.problems.p009_get_middle import get_middle

def test_get_middle():
    # Test with an odd-length list
    assert get_middle([1, 2, 3]) == 2
    assert get_middle([10, 20, 30, 40, 50]) == 30
    
    # Test with an even-length list
    assert get_middle([1, 2, 3, 4]) == 2
    assert get_middle([5, 10, 15, 20]) == 10
    
    # Test with a single element list
    assert get_middle([42]) == 42
    
    # Test with larger lists
    assert get_middle([1, 2, 3, 4, 5, 6, 7, 8, 9]) == 5
    assert get_middle([1, 2, 3, 4, 5, 6, 7, 8]) == 4
