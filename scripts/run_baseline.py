from stem_agent.evaluator import evaluate_agent, save_summary
from stem_agent.qa_agent import BaselineQAAgent


def main():
    agent = BaselineQAAgent()
    summary = evaluate_agent(agent, output_dir="runs/baseline_generated_tests")
    save_summary(summary, "runs/baseline_run.json")

    print(f"Agent: {summary.agent_name}")
    print(f"Total problems: {summary.total_problems}")
    print(f"Bugs found: {summary.bugs_found}")
    print(f"Bug detection rate: {summary.bug_detection_rate:.2%}")
    print(f"Invalid test rate: {summary.invalid_test_rate:.2%}")


if __name__ == "__main__":
    main()
