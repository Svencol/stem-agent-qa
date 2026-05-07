def reverse_words(sentence: str) -> str:
    """
    Return a string where the order of words is reversed.

    Words are separated by whitespace. Multiple spaces should be treated
    as a single separator. The returned string should use single spaces.

    Example:
        reverse_words("hello world") -> "world hello"
        reverse_words("  hello   world  ") -> "world hello"
    """
    return " ".join(sentence.split(" ")[::-1])
