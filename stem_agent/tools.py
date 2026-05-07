import subprocess
import sys
from pathlib import Path


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def run_pytest(test_file: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-q"],
        capture_output=True,
        text=True,
    )

    output = result.stdout + "\n" + result.stderr
    return result.returncode == 0, output
