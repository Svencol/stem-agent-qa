from benchmarks.problems.p007_safe_divide import safe_divide
import pytest

def test_safe_divide_normal_cases():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(15, 3) == 5.0
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(0, 1) == 0.0

def test_safe_divide_zero_divisor():
    assert safe_divide(10, 0) is None
    assert safe_divide(-10, 0) is None
    assert safe_divide(0, 0) is None

def test_safe_divide_edge_cases():
    assert safe_divide(1, 1) == 1.0
    assert safe_divide(1, -1) == -1.0
    assert safe_divide(1e10, 1e10) == 1.0
    assert safe_divide(1e-10, 1e-10) == 1.0

def test_safe_divide_stability():
    a = [10]
    b = [2]
    original_a = a.copy()
    original_b = b.copy()
    result = safe_divide(a[0], b[0])
    assert original_a == a
    assert original_b == b
    assert result == 5.0

def test_safe_divide_negative_divisor():
    assert safe_divide(10, -2) == -5.0
    assert safe_divide(-10, -2) == 5.0
