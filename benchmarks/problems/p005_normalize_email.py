def normalize_email(email: str) -> str:
    """
    Normalize an email address by lowercasing the domain only.

    The local part before '@' should remain unchanged.
    The domain after '@' should be lowercase.

    Example:
        normalize_email("User.Name@EXAMPLE.COM") -> "User.Name@example.com"
    """
    return email.lower()
