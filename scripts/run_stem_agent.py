from pathlib import Path
import shutil

from stem_agent.evaluator import evaluate_agent, save_summary
from stem_agent.qa_agent import BaselineQAAgent, SpecializedQAAgent
from stem_agent.specialize import (
    create_qa_specialization_config,
    revise_qa_specialization_config,
    propose_stopping_condition,
)


def save_config(config, path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(config.model_dump_json(indent=2), encoding="utf-8")


def rollback_to_best(best_output_dir: str, current_output_dir: str) -> str:
    """
    Preserve a regressed iteration and restore the best test files.
    Returns the rollback directory path.
    """
    rollback_dir = f"{current_output_dir}_rolled_back"

    if Path(rollback_dir).exists():
        shutil.rmtree(rollback_dir)

    shutil.move(current_output_dir, rollback_dir)

    if Path(current_output_dir).exists():
        shutil.rmtree(current_output_dir)

    shutil.copytree(best_output_dir, current_output_dir)
    return rollback_dir


def main():
    print("Running baseline agent...")
    baseline_summary = evaluate_agent(
        BaselineQAAgent(),
        output_dir="runs/stem/baseline_generated_tests",
    )
    save_summary(baseline_summary, "runs/stem/baseline_run.json")

    print("Stem agent creating initial specialization config...")
    config, domain_brief = create_qa_specialization_config()
    Path("runs/stem/domain_brief.txt").write_text(domain_brief, encoding="utf-8")
    print("  Domain brief saved.")

    print("Stem agent proposing stopping condition...")
    config.min_improvement = propose_stopping_condition(domain_brief, config.stopping_metric)
    print(f"  Self-proposed min_improvement: {config.min_improvement:.2f}")

    save_config(config, "runs/stem/specialization_config_iteration_1.json")

    best_summary = None
    best_config = config
    best_output_dir = None

    for iteration in range(1, config.max_iterations + 1):
        print(f"Running specialized agent, iteration {iteration}...")

        specialized_agent = SpecializedQAAgent(config)
        output_dir = f"runs/stem/specialized_generated_tests_iter_{iteration}"

        specialized_summary = evaluate_agent(
            specialized_agent,
            output_dir=output_dir,
        )
        save_summary(
            specialized_summary,
            f"runs/stem/specialized_run_iteration_{iteration}.json",
        )

        if best_summary is None or (
            specialized_summary.bug_detection_rate > best_summary.bug_detection_rate
        ):
            best_summary = specialized_summary
            best_config = config
            best_output_dir = output_dir
            print(f"  [STEM] New best: {best_summary.bug_detection_rate:.2%}")
        else:
            print(
                f"  [STEM] Iteration {iteration} regressed "
                f"({specialized_summary.bug_detection_rate:.2%} <= "
                f"{best_summary.bug_detection_rate:.2%}). Rolling back."
            )
            rollback_dir = rollback_to_best(best_output_dir, output_dir)
            print(f"  [STEM] Preserved regressed files in {rollback_dir}.")
            print(f"  [STEM] Restored test files from {best_output_dir}.")

        improvement = (
            specialized_summary.bug_detection_rate
            - baseline_summary.bug_detection_rate
        )

        if improvement >= config.min_improvement:
            print("Stopping rule met.")
            break

        if iteration < config.max_iterations:
            print("Stem agent revising specialization config...")
            config = revise_qa_specialization_config(
                previous_config=config,
                baseline_summary=baseline_summary,
                specialized_summary=specialized_summary,
            )
            save_config(config, f"runs/stem/specialization_config_iteration_{iteration + 1}.json")

    if best_summary is None:
        raise RuntimeError("Specialized agent did not run.")

    save_config(best_config, "runs/stem/specialization_config.json")
    save_summary(best_summary, "runs/stem/specialized_run.json")

    final_improvement = (
        best_summary.bug_detection_rate
        - baseline_summary.bug_detection_rate
    )

    print("\n=== Before / After ===")
    print(f"Baseline bug detection: {baseline_summary.bug_detection_rate:.2%}")
    print(f"Best specialized bug detection: {best_summary.bug_detection_rate:.2%}")
    print(f"Improvement: {final_improvement:.2%}")
    print(f"Invalid test rate: {best_summary.invalid_test_rate:.2%}")


if __name__ == "__main__":
    main()
