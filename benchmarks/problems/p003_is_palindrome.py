def is_palindrome(text: str) -> bool:
    """
    Return True if text is a palindrome.

    The check should ignore case, spaces, and punctuation.

    Example:
        is_palindrome("A man, a plan, a canal: Panama") -> True
    """
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]
