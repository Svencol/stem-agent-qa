import pytest
from benchmarks.problems.p018_rolling_average import rolling_average

def test_rolling_average():
    # Test with a standard case
    assert rolling_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]
    
    # Test with a larger window than the input list
    assert rolling_average([1, 2, 3], 5) == []
    
    # Test with a window size of 0 (should raise ValueError)
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], 0)
    
    # Test with a negative window size (should raise ValueError)
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], -1)
    
    # Test with a window size equal to the length of the list
    assert rolling_average([1, 2, 3], 3) == [2.0]
    
    # Test with an empty list
    assert rolling_average([], 2) == []
    
    # Test with a single element list and window size of 1
    assert rolling_average([5], 1) == [5.0]

    # Test with a larger window size than the list but with a single element
    assert rolling_average([5], 2) == []
