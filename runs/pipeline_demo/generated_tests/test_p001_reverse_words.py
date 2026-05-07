import pytest
from benchmarks.problems.p001_reverse_words import reverse_words

def test_reverse_words():
    # Test with normal input
    assert reverse_words("hello world") == "world hello"
    
    # Test with leading and trailing spaces
    assert reverse_words("  hello   world  ") == "world hello"
    
    # Test with multiple spaces between words
    assert reverse_words("hello    world") == "world hello"
    
    # Test with a single word
    assert reverse_words("hello") == "hello"
    
    # Test with an empty string
    assert reverse_words("") == ""
    
    # Test with multiple spaces only
    assert reverse_words("     ") == ""
    
    # Test with a sentence of multiple words
    assert reverse_words("The quick brown fox") == "fox brown quick The"
    
    # Test with punctuation
    assert reverse_words("Hello, world!") == "world! Hello,"
    
    # Test with a single space
    assert reverse_words(" ") == ""
    
    # Test with words separated by tabs
    assert reverse_words("hello\tworld") == "world hello"

if __name__ == "__main__":
    pytest.main()
