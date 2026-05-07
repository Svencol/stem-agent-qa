from benchmarks.problems.p008_unique_sorted import unique_sorted

def test_unique_sorted_normal_case():
    assert unique_sorted([3, 1, 3, 2]) == [1, 2, 3]

def test_unique_sorted_empty_input():
    assert unique_sorted([]) == []

def test_unique_sorted_single_element():
    assert unique_sorted([5]) == [5]

def test_unique_sorted_all_duplicates():
    assert unique_sorted([2, 2, 2, 2]) == [2]

def test_unique_sorted_negative_numbers():
    assert unique_sorted([-1, -3, -2, -1]) == [-3, -2, -1]

def test_unique_sorted_stability_check():
    original = [3, 1, 3, 2]
    copy = original.copy()
    result = unique_sorted(original)
    assert original == copy
    assert result == [1, 2, 3]
