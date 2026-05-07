import pytest
from benchmarks.problems.p012_remove_none import remove_none

def test_remove_none():
    # Test with a list containing None values
    values = [1, None, 2]
    result = remove_none(values)
    assert result == [1, 2]  # Check that None values are removed
    assert values == [1, None, 2]  # Ensure original list is unchanged

    # Test with a list that has no None values
    values = [1, 2, 3]
    result = remove_none(values)
    assert result == [1, 2, 3]  # Check that the list remains the same
    assert values == [1, 2, 3]  # Ensure original list is unchanged

    # Test with a list that is empty
    values = []
    result = remove_none(values)
    assert result == []  # Check that the result is an empty list
    assert values == []  # Ensure original list is unchanged

    # Test with a list that contains only None values
    values = [None, None, None]
    result = remove_none(values)
    assert result == []  # Check that the result is an empty list
    assert values == [None, None, None]  # Ensure original list is unchanged

    # Test with a list containing mixed types
    values = [None, 'string', 3.14, None, 42]
    result = remove_none(values)
    assert result == ['string', 3.14, 42]  # Check that None values are removed
    assert values == [None, 'string', 3.14, None, 42]  # Ensure original list is unchanged

if __name__ == "__main__":
    pytest.main()
