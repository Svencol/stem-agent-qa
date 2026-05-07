from benchmarks.problems.p019_normalize_path import normalize_path

def test_normalize_path_basic():
    assert normalize_path("/a/./b//c/../") == "/a/b"
    assert normalize_path("/../../a") == "/a"

def test_normalize_path_edge_cases():
    assert normalize_path("") == "/"
    assert normalize_path("/") == "/"
    assert normalize_path("/..") == "/"
    assert normalize_path("/../..") == "/"
    assert normalize_path("/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z") == "/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z"

def test_normalize_path_single_element():
    assert normalize_path("/a") == "/a"
    assert normalize_path("/..") == "/"

def test_normalize_path_multiple_slashes():
    assert normalize_path("//a//b//c//") == "/a/b/c"

def test_normalize_path_mutation_check():
    path = "/a/b/c/../d"
    original_path = path[:]
    normalize_path(path)
    assert path == original_path

def test_normalize_path_above_root():
    assert normalize_path("/a/b/c/../../..") == "/"
