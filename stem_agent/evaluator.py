import json
from pathlib import Path

from stem_agent.schemas import BenchmarkProblem, AgentResult, EvaluationSummary
from stem_agent.tools import run_pytest


INVALID_PATTERNS = [
    "SyntaxError",
    "ImportError",
    "ModuleNotFoundError",
    "NameError",
    "IndentationError",
    "ERROR collecting",
]


def load_benchmark(metadata_path: str = "benchmarks/metadata.json") -> list[BenchmarkProblem]:
    data = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    return [BenchmarkProblem(**item) for item in data]


def is_invalid_test_output(output: str) -> bool:
    return any(pattern in output for pattern in INVALID_PATTERNS)


def evaluate_agent(agent, output_dir: str) -> EvaluationSummary:
    problems = load_benchmark()
    results: list[AgentResult] = []

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for problem in problems:
        generated_test_file = f"{output_dir}/test_{problem.id}_{problem.name}.py"

        try:
            agent.generate_tests(problem.problem_file, generated_test_file)
            passed, output = run_pytest(generated_test_file)

            invalid_tests = is_invalid_test_output(output)
            hidden_bug_found = (not passed) and (not invalid_tests)

            result = AgentResult(
                problem_id=problem.id,
                generated_test_file=generated_test_file,
                tests_ran=True,
                hidden_bug_found=hidden_bug_found,
                invalid_tests=invalid_tests,
                notes=output[-1000:],
            )

        except Exception as exc:
            result = AgentResult(
                problem_id=problem.id,
                generated_test_file=generated_test_file,
                tests_ran=False,
                hidden_bug_found=False,
                invalid_tests=True,
                notes=str(exc),
            )

        results.append(result)

    total = len(results)
    bugs_found = sum(r.hidden_bug_found for r in results)
    invalid_tests = sum(r.invalid_tests for r in results)

    return EvaluationSummary(
        agent_name=agent.name,
        total_problems=total,
        bugs_found=bugs_found,
        invalid_test_count=invalid_tests,
        bug_detection_rate=bugs_found / total if total else 0.0,
        invalid_test_rate=invalid_tests / total if total else 0.0,
        results=results,
    )


def save_summary(summary: EvaluationSummary, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(summary.model_dump_json(indent=2), encoding="utf-8")
