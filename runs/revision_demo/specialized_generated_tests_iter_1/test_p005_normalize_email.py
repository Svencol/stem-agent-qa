from benchmarks.problems.p005_normalize_email import normalize_email

def test_normalize_email_basic():
    assert normalize_email("User.Name@EXAMPLE.COM") == "User.Name@example.com"

def test_normalize_email_no_change():
    assert normalize_email("user.name@example.com") == "user.name@example.com"

def test_normalize_email_empty_string():
    assert normalize_email("") == ""

def test_normalize_email_single_character():
    assert normalize_email("A@B.COM") == "A@b.com"

def test_normalize_email_edge_case():
    assert normalize_email("user@EXAMPLE.COM") == "user@example.com"

def test_normalize_email_input_unchanged():
    email = "User.Name@EXAMPLE.COM"
    original_email = email[:]
    normalize_email(email)
    assert email == original_email
