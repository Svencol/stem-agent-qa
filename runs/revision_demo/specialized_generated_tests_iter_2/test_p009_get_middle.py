from benchmarks.problems.p009_get_middle import get_middle
import pytest

def test_get_middle_odd_length():
    assert get_middle([1, 2, 3]) == 2

def test_get_middle_even_length():
    assert get_middle([1, 2, 3, 4]) == 2

def test_get_middle_single_element():
    assert get_middle([42]) == 42

def test_get_middle_empty_list():
    with pytest.raises(IndexError):
        get_middle([])

def test_get_middle_stability():
    values = [1, 2, 3, 4]
    original_values = values.copy()
    get_middle(values)
    assert values == original_values

def test_get_middle_large_list():
    assert get_middle(list(range(1000))) == 499
