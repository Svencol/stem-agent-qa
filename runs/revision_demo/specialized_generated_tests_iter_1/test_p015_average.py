from benchmarks.problems.p015_average import average

def test_average_normal_case():
    assert average([1, 2, 3]) == 2.0

def test_average_empty_list():
    assert average([]) is None

def test_average_single_element():
    assert average([5]) == 5.0

def test_average_negative_numbers():
    assert average([-1, -2, -3]) == -2.0

def test_average_with_zero():
    assert average([0, 0, 0]) == 0.0

def test_average_stability_check():
    values = [1, 2, 3]
    original_values = values.copy()
    average(values)
    assert values == original_values
