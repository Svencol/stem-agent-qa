def find_max(values: list[int]) -> int:
    """
    Return the maximum integer in a non-empty list.

    Example:
        find_max([1, 5, 2]) -> 5
        find_max([-10, -3, -7]) -> -3
    """
    current = 0
    for value in values:
        if value > current:
            current = value
    return current
