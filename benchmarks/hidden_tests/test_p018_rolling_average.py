import pytest

from benchmarks.problems.p018_rolling_average import rolling_average


def test_basic_window_two():
    assert rolling_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]


def test_window_equal_to_length():
    assert rolling_average([1, 2, 3], 3) == [2.0]


def test_window_larger_than_length():
    assert rolling_average([1, 2, 3], 5) == []


def test_invalid_window_raises():
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], 0)
