from benchmarks.problems.p014_is_anagram import is_anagram

def test_anagram_with_spaces_and_case():
    assert is_anagram("Dormitory", "Dirty room") == True

def test_anagram_with_different_case():
    assert is_anagram("Listen", "Silent") == True

def test_not_anagram_with_different_letters():
    assert is_anagram("Hello", "World") == False

def test_empty_strings():
    assert is_anagram("", "") == True

def test_single_character_anagram():
    assert is_anagram("a", "a") == True
    assert is_anagram("a", "b") == False

def test_anagram_with_extra_spaces():
    assert is_anagram("   A gentleman  ", "Elegant man   ") == True
