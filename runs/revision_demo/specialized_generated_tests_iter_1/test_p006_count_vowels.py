from benchmarks.problems.p006_count_vowels import count_vowels

def test_count_vowels_normal_cases():
    assert count_vowels("Hello") == 2
    assert count_vowels("AEIOU") == 5
    assert count_vowels("Python") == 1
    assert count_vowels("Programming") == 3

def test_count_vowels_edge_cases():
    assert count_vowels("") == 0
    assert count_vowels("bcd") == 0
    assert count_vowels("a") == 1
    assert count_vowels("A") == 1
    assert count_vowels("aeiouAEIOU") == 10

def test_count_vowels_stability():
    text = "Hello World"
    original_text = text[:]
    count_vowels(text)
    assert text == original_text

    text = "Python Programming"
    original_text = text[:]
    count_vowels(text)
    assert text == original_text
