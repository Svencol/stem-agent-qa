from benchmarks.problems.p003_is_palindrome import is_palindrome

def test_palindrome_normal_case():
    assert is_palindrome("A man, a plan, a canal: Panama") is True

def test_palindrome_edge_case_empty_string():
    assert is_palindrome("") is True

def test_palindrome_edge_case_single_character():
    assert is_palindrome("a") is True

def test_palindrome_edge_case_non_palindrome():
    assert is_palindrome("hello") is False

def test_palindrome_edge_case_with_spaces_and_punctuation():
    assert is_palindrome("No 'x' in Nixon") is True

def test_palindrome_stability_check():
    original = "A man, a plan, a canal: Panama"
    is_palindrome(original)
    assert original == "A man, a plan, a canal: Panama"
