import pytest
from benchmarks.problems.p016_lower_bound import lower_bound

def test_lower_bound():
    # Test cases based on the provided examples
    assert lower_bound([1, 3, 5, 7], 5) == 2
    assert lower_bound([1, 3, 5, 7], 4) == 2
    assert lower_bound([1, 3, 5, 7], 8) == 4
    
    # Additional test cases
    assert lower_bound([1, 2, 3, 4, 5], 0) == 0  # Target is less than all elements
    assert lower_bound([1, 2, 3, 4, 5], 1) == 0  # Target is equal to the first element
    assert lower_bound([1, 2, 3, 4, 5], 2) == 1  # Target is equal to the second element
    assert lower_bound([1, 2, 3, 4, 5], 5) == 4  # Target is equal to the last element
    assert lower_bound([1, 2, 3, 4, 5], 6) == 5  # Target is greater than all elements
    assert lower_bound([], 1) == 0  # Empty list case

    # Edge case: list with duplicate values
    assert lower_bound([1, 1, 1, 1, 1], 1) == 0  # Target equal to duplicates
    assert lower_bound([1, 1, 1, 1, 1], 2) == 5  # Target greater than duplicates
    assert lower_bound([1, 1, 1, 1, 1], 0) == 0  # Target less than duplicates

if __name__ == "__main__":
    pytest.main()
