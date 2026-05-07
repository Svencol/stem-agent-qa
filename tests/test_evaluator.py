from stem_agent.evaluator import evaluate_agent
from stem_agent.qa_agent import BaselineQAAgent, SpecializedQAAgent
from stem_agent.schemas import SpecializationConfig


def sample_config() -> SpecializationConfig:
    return SpecializationConfig(
        domain="python_quality_assurance",
        architecture="spec_extract_generate_execute_refine",
        tools=["read_text", "write_text", "pytest_runner"],
        skills=[
            "read_docstring_specification",
            "generate_normal_cases",
            "generate_edge_cases",
            "execute_tests",
        ],
        stopping_metric="bug_detection_rate",
        max_iterations=1,
        min_improvement=0.15,
    )


def test_baseline_evaluator_runs():
    summary = evaluate_agent(
        BaselineQAAgent(),
        output_dir="runs/test_baseline_generated_tests",
    )

    assert summary.agent_name == "baseline_qa_agent"
    assert summary.total_problems >= 5
    assert summary.invalid_test_rate == 0.0


def test_specialized_agent_requires_config():
    agent = SpecializedQAAgent(sample_config())

    assert agent.config.domain == "python_quality_assurance"
    assert "generate_edge_cases" in agent.config.skills
