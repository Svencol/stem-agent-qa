from benchmarks.problems.p019_normalize_path import normalize_path
import pytest

def test_normalize_path_basic():
    assert normalize_path("/a/./b//c/../") == "/a/b"
    assert normalize_path("/../../a") == "/a"

def test_normalize_path_empty():
    assert normalize_path("") == "/"

def test_normalize_path_single_element():
    assert normalize_path("/a") == "/a"
    assert normalize_path("/..") == "/"

def test_normalize_path_multiple_slashes():
    assert normalize_path("//a//b//c//") == "/a/b/c"

def test_normalize_path_above_root():
    assert normalize_path("/../..") == "/"

def test_normalize_path_side_effect():
    path = "/a/b/c/../.."
    original_path = path[:]
    result = normalize_path(path)
    assert path == original_path
    assert result == "/a"
