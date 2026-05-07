def count_vowels(text: str) -> int:
    """
    Count the number of vowels in a string.

    Vowels are a, e, i, o, u. The count should be case-insensitive.

    Example:
        count_vowels("Hello") -> 2
        count_vowels("AEIOU") -> 5
    """
    vowels = set("aeiou")
    return sum(1 for char in text if char in vowels)
