from unittest.mock import patch

from stem_agent.specialize import create_pipeline_spec
from stem_agent.schemas import StageType


def test_create_pipeline_spec_from_mocked_llm():
    with patch("stem_agent.specialize.call_json_model") as mock:
        mock.return_value = {
            "domain": "Python Quality Assurance",
            "stages": [
                {
                    "name": "extract_spec",
                    "stage_type": "prompt",
                    "instruction": "Extract expected behavior.",
                    "code": None,
                    "runs_on": "previous",
                },
                {
                    "name": "generate_tests",
                    "stage_type": "prompt",
                    "instruction": "Generate pytest tests.",
                    "code": None,
                    "runs_on": "previous",
                },
            ],
            "stopping_metric": "bug_detection_rate",
            "min_improvement": 0.2,
        }

        spec = create_pipeline_spec("Domain brief", "Python Quality Assurance")

    assert spec.domain == "Python Quality Assurance"
    assert len(spec.stages) == 3
    assert spec.stages[0].stage_type == StageType.prompt
    assert any(stage.stage_type == StageType.tool for stage in spec.stages)


def test_create_pipeline_spec_normalizes_missing_instruction():
    with patch("stem_agent.specialize.call_json_model") as mock:
        mock.return_value = {
            "domain": "Python Quality Assurance",
            "stages": [
                {
                    "name": "execute_tests",
                    "stage_type": "tool",
                    "instruction": None,
                    "code": "def run(input: str) -> str:\n    return input\n",
                    "runs_on": None,
                }
            ],
            "stopping_metric": "bug_detection_rate",
            "min_improvement": 0.2,
        }

        spec = create_pipeline_spec("Domain brief", "Python Quality Assurance")

    assert spec.stages[0].instruction == "Run stage execute_tests."
    assert spec.stages[0].runs_on == "previous"


def test_pipeline_normalization_removes_reporting_stage_after_test_generation():
    from stem_agent.specialize import _normalize_pipeline_data

    data = {
        "domain": "Python Quality Assurance",
        "stages": [
            {
                "name": "extract_spec",
                "stage_type": "prompt",
                "instruction": "Extract intended behavior.",
                "code": None,
                "runs_on": "previous",
            },
            {
                "name": "generate_tests",
                "stage_type": "prompt",
                "instruction": "Generate pytest tests.",
                "code": None,
                "runs_on": "previous",
            },
            {
                "name": "document_results",
                "stage_type": "prompt",
                "instruction": "Summarize the tests in prose.",
                "code": None,
                "runs_on": "previous",
            },
        ],
        "stopping_metric": "bug_detection_rate",
        "min_improvement": 0.15,
    }

    normalized = _normalize_pipeline_data(data, "Python Quality Assurance")

    assert [stage["name"] for stage in normalized["stages"]] == [
        "extract_spec",
        "extract_python_context",
        "generate_tests",
    ]
    assert "Return only valid pytest code" in normalized["stages"][-1]["instruction"]


def test_pipeline_normalization_appends_pytest_stage_if_missing():
    from stem_agent.specialize import _normalize_pipeline_data

    data = {
        "domain": "Python Quality Assurance",
        "stages": [
            {
                "name": "extract_spec",
                "stage_type": "prompt",
                "instruction": "Extract intended behavior.",
                "code": None,
                "runs_on": "previous",
            }
        ],
        "stopping_metric": "bug_detection_rate",
        "min_improvement": 0.15,
    }

    normalized = _normalize_pipeline_data(data, "Python Quality Assurance")

    assert normalized["stages"][-1]["name"] == "generate_pytest_tests"
    assert "Return only valid pytest code" in normalized["stages"][-1]["instruction"]


def test_pipeline_normalization_adds_tool_stage_for_python_qa():
    from stem_agent.specialize import _normalize_pipeline_data

    data = {
        "domain": "Python Quality Assurance",
        "stages": [
            {
                "name": "extract_spec",
                "stage_type": "prompt",
                "instruction": "Extract intended behavior.",
                "code": None,
                "runs_on": "previous",
            },
            {
                "name": "generate_tests",
                "stage_type": "prompt",
                "instruction": "Generate pytest tests.",
                "code": None,
                "runs_on": "previous",
            },
        ],
        "stopping_metric": "bug_detection_rate",
        "min_improvement": 0.15,
    }

    normalized = _normalize_pipeline_data(data, "Python Quality Assurance")

    assert any(stage["stage_type"] == "tool" for stage in normalized["stages"])
    assert any(stage["name"] == "extract_python_context" for stage in normalized["stages"])
