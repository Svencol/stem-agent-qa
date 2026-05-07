from benchmarks.problems.p001_reverse_words import reverse_words

def test_reverse_words_normal():
    assert reverse_words("hello world") == "world hello"

def test_reverse_words_with_extra_spaces():
    assert reverse_words("  hello   world  ") == "world hello"

def test_reverse_words_empty_string():
    assert reverse_words("") == ""

def test_reverse_words_single_word():
    assert reverse_words("hello") == "hello"

def test_reverse_words_single_space():
    assert reverse_words(" ") == ""

def test_reverse_words_stability():
    original = "  hello   world  "
    copy = original
    result = reverse_words(original)
    assert original == copy
    assert result == "world hello"
