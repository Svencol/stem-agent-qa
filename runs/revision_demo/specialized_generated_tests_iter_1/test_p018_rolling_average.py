from benchmarks.problems.p018_rolling_average import rolling_average
import pytest

def test_rolling_average_normal_case():
    assert rolling_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]

def test_rolling_average_empty_input():
    assert rolling_average([], 2) == []

def test_rolling_average_window_larger_than_input():
    assert rolling_average([1, 2, 3], 5) == []

def test_rolling_average_zero_window():
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], 0)

def test_rolling_average_negative_window():
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], -1)

def test_rolling_average_input_mutation():
    values = [1, 2, 3, 4]
    original_values = values.copy()
    rolling_average(values, 2)
    assert values == original_values
