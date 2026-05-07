import pytest
from benchmarks.problems.p003_is_palindrome import is_palindrome

def test_is_palindrome():
    # Test typical palindromes
    assert is_palindrome("A man, a plan, a canal: Panama") == True
    assert is_palindrome("racecar") == True
    assert is_palindrome("No 'x' in Nixon") == True
    assert is_palindrome("Was it a car or a cat I saw?") == True
    
    # Test non-palindromes
    assert is_palindrome("hello") == False
    assert is_palindrome("world") == False
    assert is_palindrome("Python") == False
    
    # Test edge cases
    assert is_palindrome("") == True  # Empty string is considered a palindrome
    assert is_palindrome(" ") == True  # Space is considered a palindrome
    assert is_palindrome("!@#$%^&*()") == True  # Only punctuation is considered a palindrome
    assert is_palindrome("A") == True  # Single character is a palindrome
    assert is_palindrome("ab") == False  # Two different characters are not a palindrome
