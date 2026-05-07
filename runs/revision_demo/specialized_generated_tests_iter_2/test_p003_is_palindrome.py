from benchmarks.problems.p003_is_palindrome import is_palindrome

def test_palindrome_normal_case():
    assert is_palindrome("A man, a plan, a canal: Panama") is True

def test_palindrome_single_character():
    assert is_palindrome("a") is True

def test_palindrome_empty_string():
    assert is_palindrome("") is True

def test_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("No 'x' in Nixon") is True

def test_not_palindrome():
    assert is_palindrome("Hello, World!") is False

def test_palindrome_case_insensitivity():
    assert is_palindrome("Able was I ere I saw Elba") is True
