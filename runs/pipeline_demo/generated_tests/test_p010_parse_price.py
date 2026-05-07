import pytest
from benchmarks.problems.p010_parse_price import parse_price

def test_parse_price_with_dollar_sign():
    assert parse_price("$1,234.50") == 1234.50

def test_parse_price_without_dollar_sign():
    assert parse_price("99.99") == 99.99

def test_parse_price_with_commas():
    assert parse_price("$12,345.67") == 12345.67
    assert parse_price("1,000.00") == 1000.00

def test_parse_price_without_commas():
    assert parse_price("1234.56") == 1234.56
    assert parse_price("$0.99") == 0.99

def test_parse_price_with_edge_cases():
    assert parse_price("$0") == 0.0
    assert parse_price("$1,000") == 1000.0
    assert parse_price("$100.00") == 100.0

def test_parse_price_invalid_input():
    with pytest.raises(ValueError):
        parse_price("invalid price")
