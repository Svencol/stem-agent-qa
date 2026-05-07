from pathlib import Path

from scripts.run_stem_agent import rollback_to_best


def test_rollback_dir_created_on_regression(tmp_path):
    best_dir = tmp_path / "iter_1"
    best_dir.mkdir()
    (best_dir / "test_foo.py").write_text("def test_foo(): assert True\n", encoding="utf-8")

    current_dir = tmp_path / "iter_2"
    current_dir.mkdir()
    (current_dir / "test_foo.py").write_text("def test_foo(): assert False\n", encoding="utf-8")

    rollback_dir = rollback_to_best(str(best_dir), str(current_dir))

    assert Path(rollback_dir).exists()
    assert (current_dir / "test_foo.py").read_text(encoding="utf-8") == "def test_foo(): assert True\n"
    assert (Path(rollback_dir) / "test_foo.py").read_text(encoding="utf-8") == "def test_foo(): assert False\n"


def test_best_is_preserved_across_regression(tmp_path):
    best_dir = tmp_path / "best"
    best_dir.mkdir()
    (best_dir / "sentinel.py").write_text("# best iteration\n", encoding="utf-8")

    regressed_dir = tmp_path / "regressed"
    regressed_dir.mkdir()
    (regressed_dir / "sentinel.py").write_text("# worse iteration\n", encoding="utf-8")

    rollback_to_best(str(best_dir), str(regressed_dir))

    assert (regressed_dir / "sentinel.py").read_text(encoding="utf-8") == "# best iteration\n"
    assert (best_dir / "sentinel.py").read_text(encoding="utf-8") == "# best iteration\n"
