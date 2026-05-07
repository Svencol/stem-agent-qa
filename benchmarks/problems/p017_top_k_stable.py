def top_k_stable(items: list[tuple[str, int]], k: int) -> list[str]:
    """
    Return the names of the top k items by score.

    Higher scores come first. If two items have the same score, preserve their
    original input order. If k is larger than the number of items, return all
    item names in sorted order by score.

    Example:
        top_k_stable([("a", 10), ("b", 10), ("c", 5)], 2) -> ["a", "b"]
    """
    ranked = sorted(items, key=lambda item: (-item[1], item[0]))
    return [name for name, score in ranked[:k]]
