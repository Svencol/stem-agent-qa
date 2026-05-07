from benchmarks.problems.p006_count_vowels import count_vowels


def test_lowercase_vowels():
    assert count_vowels("hello") == 2


def test_uppercase_vowels():
    assert count_vowels("AEIOU") == 5
