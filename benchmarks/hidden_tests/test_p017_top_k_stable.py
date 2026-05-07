from benchmarks.problems.p017_top_k_stable import top_k_stable


def test_basic_top_k():
    assert top_k_stable([("a", 10), ("b", 5), ("c", 1)], 2) == ["a", "b"]


def test_preserves_tie_order():
    assert top_k_stable([("b", 10), ("a", 10), ("c", 5)], 2) == ["b", "a"]


def test_k_larger_than_items():
    assert top_k_stable([("x", 1), ("y", 3)], 5) == ["y", "x"]
