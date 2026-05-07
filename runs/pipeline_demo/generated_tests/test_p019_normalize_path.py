import pytest
from benchmarks.problems.p019_normalize_path import normalize_path

def test_normalize_path():
    # Test cases to validate the functionality of normalize_path

    # Basic normalization
    assert normalize_path("/a/./b//c/../") == "/a/b"
    assert normalize_path("/../../a") == "/a"
    
    # Edge cases
    assert normalize_path("/") == "/"
    assert normalize_path("//") == "/"
    assert normalize_path("/a/b/c") == "/a/b/c"
    assert normalize_path("/a//b/c/./d/../") == "/a/b/c"
    
    # Going above root
    assert normalize_path("/../") == "/"
    assert normalize_path("/a/../..") == "/"
    
    # Complex paths
    assert normalize_path("/a/b/c/../../d/./e/../f") == "/a/d/f"
    assert normalize_path("/a/b/../../c/./d/e/../..") == "/c"
    
    # Multiple slashes
    assert normalize_path("///a///b/c//") == "/a/b/c"
    
    # Empty path
    assert normalize_path("") == "/"
