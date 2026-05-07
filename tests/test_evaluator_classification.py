from stem_agent.evaluator import is_invalid_test_output


def test_invalid_test_output_detects_syntax_error():
    output = "SyntaxError: invalid syntax"

    assert is_invalid_test_output(output) is True


def test_invalid_test_output_detects_import_error():
    output = "ModuleNotFoundError: No module named 'missing'"

    assert is_invalid_test_output(output) is True


def test_invalid_test_output_does_not_flag_assertion_failure():
    output = "E       AssertionError: assert 1 == 2"

    assert is_invalid_test_output(output) is False


def test_invalid_test_output_does_not_flag_value_error_from_bug():
    output = "ValueError: could not convert string to float"

    assert is_invalid_test_output(output) is False
