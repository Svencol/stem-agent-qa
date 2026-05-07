from benchmarks.problems.p010_parse_price import parse_price


def test_simple_price():
    assert parse_price("99.99") == 99.99


def test_price_with_dollar_and_comma():
    assert parse_price("$1,234.50") == 1234.50
