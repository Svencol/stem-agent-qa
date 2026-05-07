def lower_bound(values: list[int], target: int) -> int:
    """
    Return the index of the first value greater than or equal to target.

    The input list is sorted in ascending order.

    If every value is smaller than target, return len(values).

    Example:
        lower_bound([1, 3, 5, 7], 5) -> 2
        lower_bound([1, 3, 5, 7], 4) -> 2
        lower_bound([1, 3, 5, 7], 8) -> 4
    """
    left = 0
    right = len(values) - 1

    while left < right:
        mid = (left + right) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
