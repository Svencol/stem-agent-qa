import pytest
from benchmarks.problems.p007_safe_divide import safe_divide

def test_safe_divide():
    # Test normal division
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(9, 3) == 3.0
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(10, -2) == -5.0
    assert safe_divide(-10, -2) == 5.0

    # Test division by zero
    assert safe_divide(10, 0) is None
    assert safe_divide(0, 0) is None
    assert safe_divide(-10, 0) is None

    # Test division with float values
    assert safe_divide(5.0, 2.0) == 2.5
    assert safe_divide(5.0, 0.0) is None
