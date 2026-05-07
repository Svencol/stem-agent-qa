from benchmarks.problems.p012_remove_none import remove_none

def test_remove_none_with_none_values():
    values = [1, None, 2]
    result = remove_none(values)
    assert result == [1, 2]
    assert values == [1, None, 2]

def test_remove_none_with_all_none_values():
    values = [None, None, None]
    result = remove_none(values)
    assert result == []
    assert values == [None, None, None]

def test_remove_none_with_no_none_values():
    values = [1, 2, 3]
    result = remove_none(values)
    assert result == [1, 2, 3]
    assert values == [1, 2, 3]

def test_remove_none_with_empty_list():
    values = []
    result = remove_none(values)
    assert result == []
    assert values == []

def test_remove_none_with_single_none_value():
    values = [None]
    result = remove_none(values)
    assert result == []
    assert values == [None]

def test_remove_none_with_single_non_none_value():
    values = [1]
    result = remove_none(values)
    assert result == [1]
    assert values == [1]
