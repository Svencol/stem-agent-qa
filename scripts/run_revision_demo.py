from pathlib import Path

from stem_agent.evaluator import evaluate_agent, save_summary
from stem_agent.qa_agent import BaselineQAAgent, SpecializedQAAgent
from stem_agent.specialize import (
    create_qa_specialization_config,
    revise_qa_specialization_config,
)


def save_config(config, path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(config.model_dump_json(indent=2), encoding="utf-8")


def main():
    print("Running baseline agent...")
    baseline_summary = evaluate_agent(
        BaselineQAAgent(),
        output_dir="runs/revision_demo/baseline_generated_tests",
    )
    save_summary(baseline_summary, "runs/revision_demo/baseline_run.json")

    print("Creating initial specialization config...")
    config, domain_brief = create_qa_specialization_config()
    Path("runs/revision_demo/domain_brief.txt").write_text(domain_brief, encoding="utf-8")

    # Force the demo to execute revision even if the first iteration is strong.
    # This is not the production stopping rule; it is an audit/demo path.
    config.min_improvement = 1.01
    config.max_iterations = 2

    save_config(config, "runs/revision_demo/specialization_config_iteration_1.json")

    print("Running specialized agent, iteration 1...")
    agent_1 = SpecializedQAAgent(config)
    summary_1 = evaluate_agent(
        agent_1,
        output_dir="runs/revision_demo/specialized_generated_tests_iter_1",
    )
    save_summary(summary_1, "runs/revision_demo/specialized_run_iteration_1.json")

    print("Forcing revision for demonstration...")
    revised_config = revise_qa_specialization_config(
        previous_config=config,
        baseline_summary=baseline_summary,
        specialized_summary=summary_1,
    )
    revised_config.max_iterations = 2
    revised_config.min_improvement = 1.01

    save_config(revised_config, "runs/revision_demo/specialization_config_iteration_2.json")

    print("Running specialized agent, iteration 2...")
    agent_2 = SpecializedQAAgent(revised_config)
    summary_2 = evaluate_agent(
        agent_2,
        output_dir="runs/revision_demo/specialized_generated_tests_iter_2",
    )
    save_summary(summary_2, "runs/revision_demo/specialized_run_iteration_2.json")

    print("\n=== Revision Demo ===")
    print(f"Baseline bug detection: {baseline_summary.bug_detection_rate:.2%}")
    print(f"Iteration 1 bug detection: {summary_1.bug_detection_rate:.2%}")
    print(f"Iteration 2 bug detection: {summary_2.bug_detection_rate:.2%}")
    print(f"Iteration 1 invalid test rate: {summary_1.invalid_test_rate:.2%}")
    print(f"Iteration 2 invalid test rate: {summary_2.invalid_test_rate:.2%}")


if __name__ == "__main__":
    main()
