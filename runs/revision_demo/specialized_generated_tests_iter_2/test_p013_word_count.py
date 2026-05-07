from benchmarks.problems.p013_word_count import word_count

def test_basic_count():
    assert word_count("Hello, hello world!") == {"hello": 2, "world": 1}

def test_empty_string():
    assert word_count("") == {}

def test_single_word():
    assert word_count("Hello!") == {"hello": 1}

def test_case_insensitivity():
    assert word_count("Hello hello HeLLo") == {"hello": 3}

def test_punctuation_ignored():
    assert word_count("Hello, world! Hello... world?") == {"hello": 2, "world": 2}

def test_stability_of_input():
    text = "Hello, hello world!"
    original_text = text
    word_count(text)
    assert text == original_text
