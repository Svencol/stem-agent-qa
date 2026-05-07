from benchmarks.problems.p001_reverse_words import reverse_words


def test_reverse_words_basic():
    assert reverse_words("hello world") == "world hello"


def test_reverse_words_extra_spaces():
    assert reverse_words("  hello   world  ") == "world hello"
