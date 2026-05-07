def clamp(value: int, lower: int, upper: int) -> int:
    """
    Clamp value to the inclusive range [lower, upper].

    Example:
        clamp(5, 1, 10) -> 5
        clamp(-1, 0, 10) -> 0
        clamp(11, 0, 10) -> 10
    """
    if value < lower:
        return lower
    if value > upper:
        return upper - 1
    return value
