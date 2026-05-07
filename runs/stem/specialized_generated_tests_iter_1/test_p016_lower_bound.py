from benchmarks.problems.p016_lower_bound import lower_bound

def test_lower_bound_normal_cases():
    assert lower_bound([1, 3, 5, 7], 5) == 2
    assert lower_bound([1, 3, 5, 7], 4) == 2
    assert lower_bound([1, 3, 5, 7], 8) == 4

def test_lower_bound_empty_input():
    assert lower_bound([], 5) == 0

def test_lower_bound_single_element():
    assert lower_bound([3], 3) == 0
    assert lower_bound([3], 4) == 1
    assert lower_bound([3], 2) == 0

def test_lower_bound_boundary_conditions():
    assert lower_bound([1, 2, 3, 4, 5], 1) == 0
    assert lower_bound([1, 2, 3, 4, 5], 5) == 4
    assert lower_bound([1, 2, 3, 4, 5], 0) == 0
    assert lower_bound([1, 2, 3, 4, 5], 6) == 5

def test_lower_bound_stability_check():
    values = [1, 3, 5, 7]
    original_values = values.copy()
    lower_bound(values, 4)
    assert values == original_values

def test_lower_bound_duplicate_values():
    assert lower_bound([1, 2, 2, 3, 4], 2) == 1
    assert lower_bound([1, 2, 2, 3, 4], 3) == 3
    assert lower_bound([1, 2, 2, 3, 4], 5) == 5
