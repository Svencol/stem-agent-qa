import pytest
from benchmarks.problems.p017_top_k_stable import top_k_stable

def test_top_k_stable():
    # Test case 1: Basic functionality
    assert top_k_stable([("a", 10), ("b", 10), ("c", 5)], 2) == ["a", "b"]
    
    # Test case 2: k is larger than the number of items
    assert top_k_stable([("a", 10), ("b", 5)], 5) == ["a", "b"]
    
    # Test case 3: All items have the same score
    assert top_k_stable([("a", 10), ("b", 10), ("c", 10)], 2) == ["a", "b"]
    
    # Test case 4: Different scores, check order preservation
    assert top_k_stable([("a", 10), ("b", 5), ("c", 10)], 2) == ["a", "c"]
    
    # Test case 5: Empty list
    assert top_k_stable([], 3) == []
    
    # Test case 6: k is zero
    assert top_k_stable([("a", 10), ("b", 5)], 0) == []
    
    # Test case 7: Single item
    assert top_k_stable([("a", 10)], 1) == ["a"]
    
    # Test case 8: Multiple items with varying scores
    assert top_k_stable([("a", 15), ("b", 20), ("c", 15)], 3) == ["b", "a", "c"]

if __name__ == "__main__":
    pytest.main()
