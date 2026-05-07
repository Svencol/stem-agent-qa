from pathlib import Path

from stem_agent.evaluator import evaluate_agent, save_summary
from stem_agent.qa_agent import SpecializedQAAgent
from stem_agent.schemas import SpecializationConfig
from stem_agent.specialize import create_qa_specialization_config


def main():
    config_path = Path("runs/stem/specialization_config.json")

    if config_path.exists():
        config = SpecializationConfig.model_validate_json(
            config_path.read_text(encoding="utf-8")
        )
    else:
        config = create_qa_specialization_config()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config.model_dump_json(indent=2), encoding="utf-8")

    agent = SpecializedQAAgent(config)
    summary = evaluate_agent(agent, output_dir="runs/specialized_generated_tests")
    save_summary(summary, "runs/specialized_run.json")

    print(f"Agent: {summary.agent_name}")
    print(f"Total problems: {summary.total_problems}")
    print(f"Bugs found: {summary.bugs_found}")
    print(f"Bug detection rate: {summary.bug_detection_rate:.2%}")
    print(f"Invalid test rate: {summary.invalid_test_rate:.2%}")


if __name__ == "__main__":
    main()
