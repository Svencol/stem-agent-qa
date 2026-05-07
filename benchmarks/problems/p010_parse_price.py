def parse_price(price: str) -> float:
    """
    Parse a price string into a float.

    The input may start with a dollar sign and may contain commas.

    Example:
        parse_price("$1,234.50") -> 1234.50
        parse_price("99.99") -> 99.99
    """
    return float(price.replace("$", ""))
