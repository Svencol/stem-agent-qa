def normalize_path(path: str) -> str:
    """
    Normalize a Unix-style file path.

    Rules:
    - "." means current directory and should be removed.
    - ".." means parent directory and should remove the previous component.
    - Multiple slashes should be treated as one slash.
    - The result should always start with "/".
    - Going above root should stay at root.

    Example:
        normalize_path("/a/./b//c/../") -> "/a/b"
        normalize_path("/../../a") -> "/a"
    """
    parts = []
    for part in path.split("/"):
        if part == "." or part == "":
            continue
        if part == "..":
            parts.pop()
        else:
            parts.append(part)

    return "/" + "/".join(parts)
