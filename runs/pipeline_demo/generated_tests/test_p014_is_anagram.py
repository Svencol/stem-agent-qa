import pytest
from benchmarks.problems.p014_is_anagram import is_anagram

def test_is_anagram():
    # Test cases where the strings are anagrams
    assert is_anagram("Dormitory", "Dirty room") == True
    assert is_anagram("Listen", "Silent") == True
    assert is_anagram("The Morse Code", "Here come dots") == True
    assert is_anagram("Astronomer", "Moon starer") == True

    # Test cases where the strings are not anagrams
    assert is_anagram("Hello", "World") == False
    assert is_anagram("Python", "Java") == False
    assert is_anagram("Anagram", "Nag a ram!") == False  # Special characters and spaces should be ignored

    # Test cases with empty strings
    assert is_anagram("", "") == True  # Both are empty
    assert is_anagram("a", "") == False  # One is empty, one is not

    # Test cases with single characters
    assert is_anagram("a", "a") == True
    assert is_anagram("a", "b") == False

    # Test cases with different cases
    assert is_anagram("Listen", "LISTEN") == True
    assert is_anagram("Triangle", "Integral") == True

if __name__ == "__main__":
    pytest.main()
