from benchmarks.problems.p005_normalize_email import normalize_email


def test_domain_lowercase_only():
    assert normalize_email("User.Name@EXAMPLE.COM") == "User.Name@example.com"


def test_preserve_local_part():
    assert normalize_email("MixedCase@DOMAIN.COM") == "MixedCase@domain.com"
