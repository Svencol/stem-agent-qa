from benchmarks.problems.p017_top_k_stable import top_k_stable

def test_top_k_stable_normal_case():
    result = top_k_stable([("a", 10), ("b", 10), ("c", 5)], 2)
    assert result == ["a", "b"]

def test_top_k_stable_k_greater_than_items():
    result = top_k_stable([("a", 10), ("b", 5)], 5)
    assert result == ["a", "b"]

def test_top_k_stable_empty_input():
    result = top_k_stable([], 3)
    assert result == []

def test_top_k_stable_single_element():
    result = top_k_stable([("a", 10)], 1)
    assert result == ["a"]

def test_top_k_stable_duplicate_scores():
    result = top_k_stable([("a", 10), ("b", 10), ("c", 5)], 3)
    assert result == ["a", "b", "c"]

def test_top_k_stable_input_unchanged():
    items = [("a", 10), ("b", 5)]
    original_items = items.copy()
    top_k_stable(items, 1)
    assert items == original_items


def test_top_k_stable_k_zero():
    result = top_k_stable([("a", 10), ("b", 5)], 0)
    assert result == []

def test_top_k_stable_k_equals_items():
    result = top_k_stable([("a", 10), ("b", 5)], 2)
    assert result == ["a", "b"]

def test_top_k_stable_tie_breaking_order():
    result = top_k_stable([("a", 10), ("b", 10), ("c", 5), ("d", 10)], 3)
    assert result == ["a", "b", "d"]

def test_top_k_stable_negative_scores():
    result = top_k_stable([("a", -1), ("b", -2), ("c", -3)], 2)
    assert result == ["a", "b"]

def test_top_k_stable_exception_on_negative_k():
    with pytest.raises(ValueError):
        top_k_stable([("a", 10), ("b", 5)], -1)

def test_top_k_stable_inverted_example():
    result = top_k_stable([("c", 5), ("b", 10), ("a", 10)], 2)
    assert result == ["b", "a"]
