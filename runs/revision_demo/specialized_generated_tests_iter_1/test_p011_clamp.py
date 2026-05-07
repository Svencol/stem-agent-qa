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

def test_clamp_edge_case():
    assert clamp(10, 0, 10) == 10
    assert clamp(10, 0, 9) == 9
    assert clamp(0, 0, 0) == 0
    assert clamp(-1, -1, -1) == -1
