import pytest
from benchmarks.problems.p013_word_count import word_count

def test_word_count_basic():
    assert word_count("Hello, hello world!") == {"hello": 2, "world": 1}

def test_word_count_case_insensitivity():
    assert word_count("Hello hello HeLLo") == {"hello": 3}

def test_word_count_with_punctuation():
    assert word_count("Hello, world! Hello... world?") == {"hello": 2, "world": 2}

def test_word_count_empty_string():
    assert word_count("") == {}

def test_word_count_single_word():
    assert word_count("word") == {"word": 1}

def test_word_count_multiple_spaces():
    assert word_count("   Hello   world   ") == {"hello": 1, "world": 1}

def test_word_count_numbers_and_words():
    assert word_count("word 1 word 2 word 1") == {"word": 3, "1": 1, "2": 1}

def test_word_count_special_characters():
    assert word_count("Hello @world! #hello") == {"hello": 2, "world": 1}

if __name__ == "__main__":
    pytest.main()
