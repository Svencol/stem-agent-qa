def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping intervals.

    Intervals are inclusive. If one interval ends at the same point another
    begins, they should be merged.

    Example:
        merge_intervals([(1, 3), (3, 5)]) -> [(1, 5)]
    """
    if not intervals:
        return []

    intervals = sorted(intervals)
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start < last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged
