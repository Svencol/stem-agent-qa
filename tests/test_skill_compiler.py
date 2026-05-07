"""Tests for the skill compiler — the coupling layer between config and prompt."""
from stem_agent.skill_compiler import compile_skills, _SKILL_INSTRUCTIONS


def test_compile_skills_returns_string():
    result = compile_skills(["generate_edge_cases"])
    assert isinstance(result, str)
    assert len(result) > 0


def test_compile_skills_injects_known_instruction():
    result = compile_skills(["check_side_effects"])
    assert "mutate" in result.lower() or "side" in result.lower()


def test_compile_skills_always_includes_bug_detection():
    # Even if the skill list has no bug_detection entry, the compiler adds it
    result = compile_skills(["generate_edge_cases"])
    assert "bug" in result.lower()


def test_compile_skills_empty_list():
    result = compile_skills([])
    assert result == ""


def test_compile_skills_unknown_skill_uses_fallback():
    result = compile_skills(["completely_unknown_skill_xyz"])
    assert "completely_unknown_skill_xyz" in result


def test_compile_skills_deduplicates():
    result_once = compile_skills(["generate_edge_cases"])
    result_twice = compile_skills(["generate_edge_cases", "generate_edge_cases"])
    assert result_once == result_twice


def test_compile_skills_multiple_skills_all_present():
    skills = ["read_docstring_specification", "check_side_effects", "check_stability"]
    result = compile_skills(skills)
    # Each should contribute distinct content
    assert "docstring" in result.lower() or "spec" in result.lower()
    assert "mutate" in result.lower() or "side" in result.lower()
    assert "stab" in result.lower() or "order" in result.lower() or "insertion" in result.lower()


def test_all_known_skills_compile_without_error():
    for skill in _SKILL_INSTRUCTIONS:
        result = compile_skills([skill])
        assert isinstance(result, str)
        assert len(result) > 0
