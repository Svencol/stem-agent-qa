from benchmarks.problems.p011_clamp import clamp
import pytest

def test_clamp_within_bounds():
    assert clamp(5, 1, 10) == 5

def test_clamp_below_lower_bound():
    assert clamp(-1, 0, 10) == 0

def test_clamp_above_upper_bound():
    assert clamp(11, 0, 10) == 9

def test_clamp_at_lower_bound():
    assert clamp(0, 0, 10) == 0

def test_clamp_at_upper_bound():
    assert clamp(10, 0, 10) == 10

def test_clamp_edge_case_one_below_lower():
    assert clamp(-1, 0, 10) == 0

def test_clamp_edge_case_one_above_upper():
    assert clamp(11, 0, 10) == 9


def test_clamp_mutation():
    value = [5]
    clamp(value[0], 1, 10)
    assert value[0] == 5  # Ensure the input list is not mutated

def test_clamp_stability():
    assert clamp(5, 1, 10) == 5  # Check that the order is preserved
    assert clamp(10, 0, 10) == 10  # Check that the order is preserved at upper bound

def test_clamp_edge_case_lower_bound():
    assert clamp(1, 1, 10) == 1  # Test value exactly at lower bound

def test_clamp_edge_case_upper_bound():
    assert clamp(9, 0, 10) == 9  # Test value exactly one below upper bound

def test_clamp_exception_on_invalid_input():
    with pytest.raises(TypeError):
        clamp("string", 0, 10)  # Test with a string input

def test_clamp_inverted_arguments():
    assert clamp(10, 10, 0) == 10  # Test with inverted bounds
    assert clamp(5, 10, 0) == 10  # Test with inverted bounds and value below upper
