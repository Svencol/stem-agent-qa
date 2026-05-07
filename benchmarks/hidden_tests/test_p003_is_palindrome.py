from benchmarks.problems.p003_is_palindrome import is_palindrome


def test_simple_palindrome():
    assert is_palindrome("Racecar") is True


def test_punctuation_palindrome():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
