from benchmarks.problems.p001_reverse_words import reverse_words


def test_basic():
    assert reverse_words("hello world") == "world hello"


def test_extra_spaces():
    assert reverse_words("  hello   world  ") == "world hello"
