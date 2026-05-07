def word_count(text: str) -> dict[str, int]:
    """
    Count words in a string.

    Counting should be case-insensitive and punctuation should be ignored.

    Example:
        word_count("Hello, hello world!") -> {"hello": 2, "world": 1}
    """
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
