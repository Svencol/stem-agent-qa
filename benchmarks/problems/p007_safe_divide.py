def safe_divide(a: float, b: float) -> float | None:
    """
    Divide a by b.

    If b is zero, return None instead of raising an exception.

    Example:
        safe_divide(10, 2) -> 5.0
        safe_divide(10, 0) -> None
    """
    return a / b
