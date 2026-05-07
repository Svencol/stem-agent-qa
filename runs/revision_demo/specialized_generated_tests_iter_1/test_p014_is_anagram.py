from benchmarks.problems.p014_is_anagram import is_anagram

def test_anagram_with_spaces_and_case():
    assert is_anagram("Dormitory", "Dirty room") == True

def test_anagram_with_different_cases():
    assert is_anagram("Listen", "Silent") == True

def test_anagram_with_empty_strings():
    assert is_anagram("", "") == True

def test_anagram_with_single_character():
    assert is_anagram("a", "a") == True
    assert is_anagram("a", "b") == False

def test_anagram_with_non_anagram_strings():
    assert is_anagram("hello", "world") == False

def test_anagram_with_spaces_only():
    assert is_anagram("   ", "   ") == True
    assert is_anagram("   a", "a   ") == True
