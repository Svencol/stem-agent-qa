from benchmarks.problems.p014_is_anagram import is_anagram


def test_simple_anagram():
    assert is_anagram("listen", "silent") is True


def test_ignores_spaces_and_case():
    assert is_anagram("Dormitory", "Dirty room") is True
