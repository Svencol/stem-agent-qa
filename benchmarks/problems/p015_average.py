def average(values: list[float]) -> float | None:
    """
    Return the arithmetic mean of a list of numbers.

    If the list is empty, return None.

    Example:
        average([1, 2, 3]) -> 2.0
        average([]) -> None
    """
    return sum(values) / len(values)
