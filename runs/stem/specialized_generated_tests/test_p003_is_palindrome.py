from benchmarks.problems.p003_is_palindrome import is_palindrome


def test_simple():
    assert is_palindrome("Racecar") is True


def test_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
