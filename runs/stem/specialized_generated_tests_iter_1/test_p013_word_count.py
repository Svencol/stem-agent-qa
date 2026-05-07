from benchmarks.problems.p013_word_count import word_count

def test_normal_case():
    assert word_count("Hello, hello world!") == {"hello": 2, "world": 1}

def test_empty_string():
    assert word_count("") == {}

def test_single_word():
    assert word_count("Hello!") == {"hello": 1}

def test_case_insensitivity():
    assert word_count("Hello hello HeLLo") == {"hello": 3}

def test_punctuation_ignored():
    assert word_count("Hello, world! Hello...") == {"hello": 2, "world": 1}

def test_stability_of_input():
    text = "Hello, hello world!"
    original_text = text
    result = word_count(text)
    assert text == original_text  # Ensure input is unchanged
    assert result == {"hello": 2, "world": 1}
