"""
make_report_tables.py
---------------------
Generates reports/results_table.md from saved run artifacts.
Now includes repair-pass stats and LLM-judge scores.
"""

import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fmt(rate: float) -> str:
    return f"{rate:.2%}"


def main():
    base_path    = "runs/stem/baseline_run.json"
    spec_path    = "runs/stem/specialized_run.json"

    if not Path(base_path).exists() or not Path(spec_path).exists():
        print("Run scripts/run_stem_agent.py first.")
        return

    base = load(base_path)
    spec = load(spec_path)

    lines = ["# Results\n"]

    # --- Primary table ---
    lines.append("## Bug Detection")
    lines.append("")
    lines.append(
        "| Agent | Problems | Bugs Found | Detection Rate | Invalid Rate |"
    )
    lines.append("|---|---:|---:|---:|---:|")

    for d, label in [(base, "Baseline QA Agent"), (spec, "Stem-specialized QA Agent")]:
        lines.append(
            f"| {label} "
            f"| {d['total_problems']} "
            f"| {d['bugs_found']} "
            f"| {fmt(d['bug_detection_rate'])} "
            f"| {fmt(d['invalid_test_rate'])} |"
        )

    improvement = spec["bug_detection_rate"] - base["bug_detection_rate"]
    lines.append("")
    lines.append(f"**Improvement: {improvement:.2%}**")
    lines.append("")

    # --- Repair stats ---
    if spec.get("total_repair_passes", 0) > 0:
        lines.append("## Repair Loop")
        lines.append("")
        lines.append(
            f"Total repair passes used: {spec['total_repair_passes']}  "
        )
        lines.append(
            f"Bugs found via repair: {spec['bugs_found_via_repair']}"
        )
        lines.append("")

    # --- Judge scores ---
    if spec.get("avg_judge_specificity", 0) > 0:
        lines.append("## LLM-Judge Scores (specialized agent, 1–5)")
        lines.append("")
        lines.append("| Dimension | Score |")
        lines.append("|---|---:|")
        lines.append(f"| Specificity   | {spec['avg_judge_specificity']} |")
        lines.append(f"| Coverage      | {spec['avg_judge_coverage']} |")
        lines.append(f"| Actionability | {spec['avg_judge_actionability']} |")
        lines.append("")

    output = "\n".join(lines)
    Path("reports/results_table.md").write_text(output, encoding="utf-8")
    print("Written to reports/results_table.md")
    print(output)


if __name__ == "__main__":
    main()
