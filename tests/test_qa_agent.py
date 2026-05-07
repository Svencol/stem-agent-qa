from stem_agent.qa_agent import SpecializedQAAgent, BaselineQAAgent, module_path_from_file, _clean_test_code
from stem_agent.schemas import SpecializationConfig


def sample_config() -> SpecializationConfig:
    return SpecializationConfig(
        domain="python_quality_assurance",
        architecture="spec_extract_generate_execute_refine",
        tools=["read_text", "write_text", "pytest_runner"],
        skills=["read_docstring_specification", "generate_edge_cases",
                "check_side_effects", "bug_detection"],
        stopping_metric="bug_detection_rate",
        max_iterations=1,
        min_improvement=0.15,
    )


def test_module_path_from_file_handles_forward_slashes():
    assert (
        module_path_from_file("benchmarks/problems/p001_reverse_words.py")
        == "benchmarks.problems.p001_reverse_words"
    )


def test_module_path_from_file_handles_windows_path():
    assert (
        module_path_from_file(r"benchmarks\problems\p001_reverse_words.py")
        == "benchmarks.problems.p001_reverse_words"
    )


def test_clean_test_code_removes_python_markdown_fence():
    raw = "```python\ndef test_example():\n    assert 1 + 1 == 2\n```"
    cleaned = _clean_test_code(raw)
    assert cleaned == "def test_example():\n    assert 1 + 1 == 2\n"


def test_clean_test_code_removes_plain_markdown_fence():
    raw = "```\ndef test_example():\n    assert True\n```"
    cleaned = _clean_test_code(raw)
    assert cleaned == "def test_example():\n    assert True\n"


def test_clean_test_code_extracts_fence_after_explanation():
    raw = "Here are the tests:\n```python\ndef test_example():\n    assert True\n```"
    cleaned = _clean_test_code(raw)
    assert cleaned == "def test_example():\n    assert True\n"


def test_clean_test_code_no_fence_passthrough():
    raw = "def test_foo():\n    assert True"
    cleaned = _clean_test_code(raw)
    assert cleaned == "def test_foo():\n    assert True\n"


def test_specialized_agent_builds_system_prompt_with_skills():
    agent = SpecializedQAAgent(sample_config())
    prompt = agent._build_system_prompt()
    # Compiled skills should appear as concrete instructions, not raw JSON
    assert "STEP" in prompt or "side" in prompt.lower() or "edge" in prompt.lower()
    # Should NOT be dumping raw JSON skill names
    assert '"skills"' not in prompt


def test_specialized_agent_config_accessible():
    agent = SpecializedQAAgent(sample_config())
    assert agent.config.domain == "python_quality_assurance"
    assert "check_side_effects" in agent.config.skills


def test_baseline_agent_name():
    assert BaselineQAAgent.name == "baseline_qa_agent"


def test_specialized_agent_name():
    assert SpecializedQAAgent.name == "stem_specialized_qa_agent"
