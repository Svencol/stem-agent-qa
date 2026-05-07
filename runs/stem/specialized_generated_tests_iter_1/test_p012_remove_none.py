from benchmarks.problems.p012_remove_none import remove_none

def test_remove_none_normal_case():
    assert remove_none([1, None, 2]) == [1, 2]

def test_remove_none_empty_list():
    assert remove_none([]) == []

def test_remove_none_single_element_none():
    assert remove_none([None]) == []

def test_remove_none_single_element_non_none():
    assert remove_none([1]) == [1]

def test_remove_none_multiple_nones():
    assert remove_none([None, None, 1, 2, None]) == [1, 2]

def test_remove_none_input_unchanged():
    values = [1, None, 2]
    original_values = values.copy()
    remove_none(values)
    assert values == original_values
