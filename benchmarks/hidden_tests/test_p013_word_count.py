from benchmarks.problems.p013_word_count import word_count


def test_basic_count():
    assert word_count("hello hello world") == {"hello": 2, "world": 1}


def test_ignores_punctuation():
    assert word_count("Hello, hello world!") == {"hello": 2, "world": 1}
