from pathlib import Path

from stem_agent.tools import read_text, write_text, run_pytest


def test_read_and_write_text(tmp_path):
    path = tmp_path / "example.txt"

    write_text(str(path), "hello")

    assert read_text(str(path)) == "hello"


def test_run_pytest_detects_passing_test(tmp_path):
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "def test_passes():\n"
        "    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )

    passed, output = run_pytest(str(test_file))

    assert passed is True
    assert "passed" in output


def test_run_pytest_detects_failing_test(tmp_path):
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "def test_fails():\n"
        "    assert 1 + 1 == 3\n",
        encoding="utf-8",
    )

    passed, output = run_pytest(str(test_file))

    assert passed is False
    assert "failed" in output
