import pytest
from benchmarks.problems.p006_count_vowels import count_vowels

def test_count_vowels():
    # Test with mixed case
    assert count_vowels("Hello") == 2
    assert count_vowels("AEIOU") == 5
    assert count_vowels("Python") == 1
    assert count_vowels("Vowels") == 2
    assert count_vowels("xyz") == 0
    assert count_vowels("") == 0
    assert count_vowels("aAeEiIoOuU") == 10
    assert count_vowels("12345") == 0
    assert count_vowels("A quick brown fox jumps over the lazy dog") == 11
