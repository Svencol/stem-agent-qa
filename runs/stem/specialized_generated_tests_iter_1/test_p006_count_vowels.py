from benchmarks.problems.p006_count_vowels import count_vowels

def test_count_vowels_normal_cases():
    assert count_vowels("Hello") == 2
    assert count_vowels("AEIOU") == 5
    assert count_vowels("Python") == 1
    assert count_vowels("Programming") == 3

def test_count_vowels_empty_string():
    assert count_vowels("") == 0

def test_count_vowels_single_character():
    assert count_vowels("a") == 1
    assert count_vowels("b") == 0
    assert count_vowels("A") == 1

def test_count_vowels_case_insensitivity():
    assert count_vowels("HeLLo") == 2
    assert count_vowels("aeiou") == 5

def test_count_vowels_edge_cases():
    assert count_vowels("xyz") == 0
    assert count_vowels("a" * 1000) == 1000

def test_count_vowels_stability_check():
    input_text = "Hello World"
    original_text = input_text[:]
    count_vowels(input_text)
    assert input_text == original_text
