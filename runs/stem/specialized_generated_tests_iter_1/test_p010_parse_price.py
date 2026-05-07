from benchmarks.problems.p010_parse_price import parse_price
import pytest

def test_parse_price_normal_cases():
    assert parse_price("$1,234.50") == 1234.50
    assert parse_price("99.99") == 99.99
    assert parse_price("$0.99") == 0.99
    assert parse_price("1,000") == 1000.0

def test_parse_price_edge_cases():
    assert parse_price("$0") == 0.0
    assert parse_price("") == 0.0  # Assuming empty string returns 0.0
    assert parse_price("$1") == 1.0
    assert parse_price("$100,000.00") == 100000.00

def test_parse_price_side_effects():
    price_input = "$1,234.50"
    original_price_input = price_input
    parse_price(price_input)
    assert price_input == original_price_input  # Ensure input is unchanged

    price_input = "99.99"
    original_price_input = price_input
    parse_price(price_input)
    assert price_input == original_price_input  # Ensure input is unchanged
