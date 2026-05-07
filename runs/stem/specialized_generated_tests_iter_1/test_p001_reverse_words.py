from benchmarks.problems.p001_reverse_words import reverse_words

def test_normal_case():
    assert reverse_words("hello world") == "world hello"

def test_leading_and_trailing_spaces():
    assert reverse_words("  hello   world  ") == "world hello"

def test_single_word():
    assert reverse_words("hello") == "hello"

def test_empty_string():
    assert reverse_words("") == ""

def test_multiple_spaces_only():
    assert reverse_words("     ") == ""

def test_side_effect_on_input():
    sentence = "hello world"
    original_sentence = sentence
    reverse_words(sentence)
    assert sentence == original_sentence
