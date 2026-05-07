from benchmarks.problems.p007_safe_divide import safe_divide
import pytest

def test_safe_divide_normal_cases():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(10, -2) == -5.0
    assert safe_divide(0, 5) == 0.0

def test_safe_divide_zero_divisor():
    assert safe_divide(10, 0) is None
    assert safe_divide(-10, 0) is None
    assert safe_divide(0, 0) is None

def test_safe_divide_edge_cases():
    assert safe_divide(1, 1) == 1.0
    assert safe_divide(1, 0.1) == 10.0
    assert safe_divide(1, -0.1) == -10.0

def test_safe_divide_stability():
    a = 10
    b = 2
    original_a = a
    original_b = b
    result = safe_divide(a, b)
    assert result == 5.0
    assert a == original_a
    assert b == original_b

def test_safe_divide_negative_divisor():
    assert safe_divide(10, -5) == -2.0
    assert safe_divide(-10, -5) == 2.0

def test_safe_divide_float_values():
    assert safe_divide(5.5, 2.2) == 2.5
    assert safe_divide(7.0, 0.5) == 14.0
