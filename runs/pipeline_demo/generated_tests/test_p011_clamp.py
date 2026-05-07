import pytest
from benchmarks.problems.p011_clamp import clamp

def test_clamp():
    # Test cases where the value is within the range
    assert clamp(5, 1, 10) == 5
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 1, 10) == 9  # upper bound case

    # Test cases where the value is below the lower bound
    assert clamp(-1, 0, 10) == 0
    assert clamp(-5, -3, 3) == -3  # lower bound case

    # Test cases where the value is above the upper bound
    assert clamp(11, 0, 10) == 9
    assert clamp(15, 5, 10) == 9  # upper bound case

    # Edge cases
    assert clamp(1, 1, 10) == 1  # lower bound edge case
    assert clamp(10, 1, 10) == 9  # upper bound edge case
    assert clamp(5, 5, 5) == 5  # equal bounds case

if __name__ == "__main__":
    pytest.main()
