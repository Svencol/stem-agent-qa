from benchmarks.problems.p003_is_palindrome import is_palindrome

def test_palindrome_normal_case():
    assert is_palindrome("A man, a plan, a canal: Panama") == True

def test_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("No 'x' in Nixon") == True

def test_non_palindrome():
    assert is_palindrome("Hello, World!") == False

def test_empty_string():
    assert is_palindrome("") == True

def test_single_character():
    assert is_palindrome("a") == True

def test_case_insensitivity():
    assert is_palindrome("RaceCar") == True

def test_stability_of_input():
    original = "A man, a plan, a canal: Panama"
    is_palindrome(original)
    assert original == "A man, a plan, a canal: Panama"
