def get_middle(values: list[int]) -> int:
    """
    Return the middle element of a non-empty list.

    For even-length lists, return the left middle element.

    Example:
        get_middle([1, 2, 3]) -> 2
        get_middle([1, 2, 3, 4]) -> 2
    """
    return values[len(values) // 2]
