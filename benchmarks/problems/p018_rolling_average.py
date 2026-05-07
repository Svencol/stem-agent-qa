def rolling_average(values: list[float], window: int) -> list[float]:
    """
    Return rolling averages over a fixed-size window.

    The result should contain one average for every complete window.

    If window is larger than the input length, return an empty list.
    If window is less than or equal to zero, raise ValueError.

    Example:
        rolling_average([1, 2, 3, 4], 2) -> [1.5, 2.5, 3.5]
        rolling_average([1, 2, 3], 5) -> []
    """
    if window <= 0:
        return []

    result = []
    for i in range(len(values) - window):
        result.append(sum(values[i:i + window]) / window)
    return result
