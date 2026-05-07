from benchmarks.problems.p005_normalize_email import normalize_email


def test_lowercase_domain():
    assert normalize_email("User.Name@EXAMPLE.COM") == "User.Name@example.com"


def test_preserve_local_part_case():
    assert normalize_email("MixedCase@DOMAIN.COM") == "MixedCase@domain.com"
