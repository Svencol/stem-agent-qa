from pathlib import Path

from stem_agent.domain_scout import scout_domain
from stem_agent.evaluator import evaluate_agent, save_summary
from stem_agent.pipeline_agent import DynamicPipelineAgent
from stem_agent.specialize import create_pipeline_spec


def main():
    print("Scouting domain...")
    domain_brief = scout_domain("Python Quality Assurance")

    output_root = Path("runs/pipeline_demo")
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "domain_brief.txt").write_text(domain_brief, encoding="utf-8")

    print("Creating pipeline spec...")
    spec = create_pipeline_spec(domain_brief, "Python Quality Assurance")
    (output_root / "pipeline_spec.json").write_text(
        spec.model_dump_json(indent=2),
        encoding="utf-8",
    )

    print("Running dynamic pipeline agent...")
    agent = DynamicPipelineAgent(spec)
    summary = evaluate_agent(
        agent,
        output_dir="runs/pipeline_demo/generated_tests",
    )
    save_summary(summary, "runs/pipeline_demo/pipeline_run.json")

    print("\n=== Pipeline Demo ===")
    print(f"Stages: {len(spec.stages)}")
    for stage in spec.stages:
        print(f"- {stage.name}: {stage.stage_type}")

    print(f"Bug detection: {summary.bug_detection_rate:.2%}")
    print(f"Invalid test rate: {summary.invalid_test_rate:.2%}")


if __name__ == "__main__":
    main()
