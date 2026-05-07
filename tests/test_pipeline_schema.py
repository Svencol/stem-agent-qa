from stem_agent.schemas import PipelineSpec, PipelineStage, StageType


def test_pipeline_spec_accepts_prompt_and_tool_stages():
    spec = PipelineSpec(
        domain="Python QA",
        stages=[
            PipelineStage(
                name="extract_spec",
                stage_type=StageType.prompt,
                instruction="Extract invariants.",
            ),
            PipelineStage(
                name="execute",
                stage_type=StageType.tool,
                instruction="Run the generated tests.",
                code="def run(input: str) -> str:\n    return input\n",
            ),
        ],
        stopping_metric="bug_detection_rate",
        min_improvement=0.2,
    )

    assert spec.domain == "Python QA"
    assert len(spec.stages) == 2
    assert spec.stages[1].stage_type == StageType.tool
