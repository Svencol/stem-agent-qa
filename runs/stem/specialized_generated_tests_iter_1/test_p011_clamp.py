from benchmarks.problems.p011_clamp import clamp
import pytest

def test_clamp_within_bounds():
    assert clamp(5, 1, 10) == 5

def test_clamp_below_lower_bound():
    assert clamp(-1, 0, 10) == 0

def test_clamp_above_upper_bound():
    assert clamp(11, 0, 10) == 10

def test_clamp_equal_to_lower_bound():
    assert clamp(0, 0, 10) == 0

def test_clamp_equal_to_upper_bound():
    assert clamp(10, 0, 10) == 10

def test_clamp_edge_case():
    assert clamp(10, 0, 10) == 10
    assert clamp(9, 0, 10) == 9
    assert clamp(11, 0, 10) == 10

def test_clamp_mutation_check():
    original_value = 5
    original_lower = 1
    original_upper = 10
    clamp(original_value, original_lower, original_upper)
    assert original_value == 5
    assert original_lower == 1
    assert original_upper == 10
