import pytest
from benchmarks.problems.p005_normalize_email import normalize_email

def test_normalize_email():
    # Test cases to validate the functionality of normalize_email
    assert normalize_email("User.Name@EXAMPLE.COM") == "User.Name@example.com"
    assert normalize_email("user.name@domain.com") == "user.name@domain.com"  # already normalized
    assert normalize_email("USER@EXAMPLE.COM") == "USER@example.com"
    assert normalize_email("test.email+alex@GMAIL.COM") == "test.email+alex@gmail.com"
    assert normalize_email("simple@example.com") == "simple@example.com"  # already normalized
    assert normalize_email("MixedCase@Domain.COM") == "MixedCase@domain.com"
