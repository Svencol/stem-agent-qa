from benchmarks.problems.p017_top_k_stable import top_k_stable

def test_top_k_stable_normal_case():
    assert top_k_stable([("a", 10), ("b", 10), ("c", 5)], 2) == ["a", "b"]

def test_top_k_stable_edge_case_k_greater_than_items():
    assert top_k_stable([("a", 10), ("b", 5)], 5) == ["a", "b"]

def test_top_k_stable_edge_case_empty_input():
    assert top_k_stable([], 3) == []

def test_top_k_stable_edge_case_single_element():
    assert top_k_stable([("a", 10)], 1) == ["a"]

def test_top_k_stable_edge_case_duplicate_scores():
    assert top_k_stable([("a", 10), ("b", 10), ("c", 5)], 3) == ["a", "b", "c"]

def test_top_k_stable_side_effect():
    items = [("a", 10), ("b", 5)]
    original_items = items.copy()
    top_k_stable(items, 1)
    assert items == original_items


def test_top_k_stable_stability():
    items = [("a", 10), ("b", 10), ("c", 5), ("d", 10)]
    result = top_k_stable(items, 3)
    assert result == ["a", "b", "d"]  # Check if order is preserved for ties

def test_top_k_stable_off_by_one_boundary():
    assert top_k_stable([("a", 10), ("b", 5)], 2) == ["a", "b"]  # k equals number of items
    assert top_k_stable([("a", 10), ("b", 5)], 1) == ["a"]  # k is one less than number of items

def test_top_k_stable_exception_contract():
    import pytest
    with pytest.raises(TypeError):
        top_k_stable([("a", 10), ("b", 5)], "two")  # k should be an integer
    with pytest.raises(ValueError):
        top_k_stable([("a", 10), ("b", 5)], -1)  # k should not be negative

def test_top_k_stable_inverted_example():
    assert top_k_stable([("b", 10), ("a", 10), ("c", 5)], 2) == ["b", "a"]  # Inverted order of items
