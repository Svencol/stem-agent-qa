from benchmarks.problems.p008_unique_sorted import unique_sorted
import pytest

def test_unique_sorted_normal_case():
    assert unique_sorted([3, 1, 3, 2]) == [1, 2, 3]

def test_unique_sorted_empty_input():
    assert unique_sorted([]) == []

def test_unique_sorted_single_element():
    assert unique_sorted([5]) == [5]

def test_unique_sorted_duplicates():
    assert unique_sorted([1, 1, 2, 2, 3, 3]) == [1, 2, 3]

def test_unique_sorted_negative_numbers():
    assert unique_sorted([-1, -3, -2, -1]) == [-3, -2, -1]

def test_unique_sorted_input_mutation():
    original = [3, 1, 3, 2]
    unique_sorted(original)
    assert original == [3, 1, 3, 2]
