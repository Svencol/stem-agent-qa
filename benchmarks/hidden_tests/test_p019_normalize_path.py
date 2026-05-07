from benchmarks.problems.p019_normalize_path import normalize_path


def test_removes_dot_and_double_slashes():
    assert normalize_path("/a/./b//c/../") == "/a/b"


def test_parent_at_root_stays_root():
    assert normalize_path("/../../a") == "/a"


def test_root_path():
    assert normalize_path("/") == "/"
