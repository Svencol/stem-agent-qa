import pytest
from benchmarks.problems.p015_average import average

def test_average_with_numbers():
    assert average([1, 2, 3]) == 2.0
    assert average([10, 20, 30, 40]) == 25.0
    assert average([-1, 0, 1]) == 0.0
    assert average([1.5, 2.5, 3.5]) == 2.5

def test_average_with_empty_list():
    assert average([]) is None

def test_average_with_single_element():
    assert average([5]) == 5.0
    assert average([-3]) == -3.0
