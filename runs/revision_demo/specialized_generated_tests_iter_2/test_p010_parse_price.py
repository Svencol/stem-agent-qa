from benchmarks.problems.p010_parse_price import parse_price
import pytest

def test_parse_price_with_dollar_sign_and_commas():
    assert parse_price("$1,234.50") == 1234.50

def test_parse_price_without_dollar_sign():
    assert parse_price("99.99") == 99.99

def test_parse_price_with_empty_string():
    with pytest.raises(ValueError):
        parse_price("")

def test_parse_price_with_single_element():
    assert parse_price("$0.01") == 0.01

def test_parse_price_with_only_dollar_sign():
    with pytest.raises(ValueError):
        parse_price("$")

def test_parse_price_with_invalid_characters():
    with pytest.raises(ValueError):
        parse_price("$1,234.50abc")
