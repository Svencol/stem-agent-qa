from benchmarks.problems.p004_find_max import find_max
import pytest

def test_find_max_normal_cases():
    assert find_max([1, 5, 2]) == 5
    assert find_max([-10, -3, -7]) == -3
    assert find_max([0, 0, 0]) == 0
    assert find_max([100, 200, 150]) == 200

def test_find_max_edge_cases():
    assert find_max([1]) == 1
    assert find_max([-1]) == -1
    assert find_max([1, 2]) == 2
    assert find_max([2, 1]) == 2

def test_find_max_empty_input():
    with pytest.raises(ValueError):
        find_max([])

def test_find_max_single_element():
    assert find_max([42]) == 42

def test_find_max_mutation_check():
    original_list = [1, 2, 3]
    copy_list = original_list.copy()
    find_max(original_list)
    assert original_list == copy_list
