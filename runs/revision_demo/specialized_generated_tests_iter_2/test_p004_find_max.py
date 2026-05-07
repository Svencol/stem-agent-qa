from benchmarks.problems.p004_find_max import find_max
import pytest

def test_find_max_normal_cases():
    assert find_max([1, 5, 2]) == 5
    assert find_max([-10, -3, -7]) == -3

def test_find_max_single_element():
    assert find_max([42]) == 42

def test_find_max_empty_input():
    with pytest.raises(ValueError):
        find_max([])

def test_find_max_mutation_check():
    values = [1, 2, 3]
    original_values = values.copy()
    find_max(values)
    assert values == original_values

def test_find_max_boundary_conditions():
    assert find_max([0, 1]) == 1
    assert find_max([-1, 0]) == 0

def test_find_max_duplicate_values():
    assert find_max([1, 1, 1]) == 1
    assert find_max([2, 2, 3, 2]) == 3
