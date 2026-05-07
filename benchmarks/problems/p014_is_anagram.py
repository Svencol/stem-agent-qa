def is_anagram(a: str, b: str) -> bool:
    """
    Return True if two strings are anagrams.

    The check should ignore spaces and case.

    Example:
        is_anagram("Dormitory", "Dirty room") -> True
    """
    return sorted(a.lower()) == sorted(b.lower())
