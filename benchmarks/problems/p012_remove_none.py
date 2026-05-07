def remove_none(values: list[object]) -> list[object]:
    """
    Return a new list with all None values removed.

    The function should not mutate the input list.

    Example:
        values = [1, None, 2]
        remove_none(values) -> [1, 2]
        values should remain [1, None, 2]
    """
    while None in values:
        values.remove(None)
    return values
