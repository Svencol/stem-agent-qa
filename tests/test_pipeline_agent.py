from unittest.mock import patch

from stem_agent.pipeline_agent import DynamicPipelineAgent
from stem_agent.schemas import PipelineSpec, PipelineStage, StageType


def test_dynamic_pipeline_agent_runs_tool_stage():
    spec = PipelineSpec(
        domain="toy",
        stages=[
            PipelineStage(
                name="uppercase",
                stage_type=StageType.tool,
                instruction="Uppercase input.",
                code="def run(input: str) -> str:\n    return input.upper()\n",
            )
        ],
        stopping_metric="toy_metric",
    )

    agent = DynamicPipelineAgent(spec)

    assert agent.run("hello") == "HELLO"


def test_dynamic_pipeline_agent_runs_prompt_stage():
    spec = PipelineSpec(
        domain="toy",
        stages=[
            PipelineStage(
                name="prompt",
                stage_type=StageType.prompt,
                instruction="Rewrite input.",
            )
        ],
        stopping_metric="toy_metric",
    )

    agent = DynamicPipelineAgent(spec)

    with patch("stem_agent.pipeline_agent.call_text_model") as mock:
        mock.return_value = "rewritten"
        result = agent.run("original")

    assert result == "rewritten"
    mock.assert_called_once()


def test_dynamic_pipeline_agent_tool_compile_failure_does_not_crash():
    spec = PipelineSpec(
        domain="toy",
        stages=[
            PipelineStage(
                name="bad_tool",
                stage_type=StageType.tool,
                instruction="Broken tool.",
                code="def run(input: str) -> str:\n    return ???\n",
            )
        ],
        stopping_metric="toy_metric",
    )

    agent = DynamicPipelineAgent(spec)
    result = agent.run("hello")

    assert "tool bad_tool failed" in result
    assert "hello" in result


def test_looks_like_valid_pytest_rejects_prose():
    from stem_agent.pipeline_agent import _looks_like_valid_pytest

    assert _looks_like_valid_pytest("Here are some tests you could write.") is False


def test_looks_like_valid_pytest_accepts_test_function():
    from stem_agent.pipeline_agent import _looks_like_valid_pytest

    code = "def test_example():\n    assert True\n"

    assert _looks_like_valid_pytest(code) is True
