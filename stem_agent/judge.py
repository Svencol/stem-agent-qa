"""
judge.py
--------
LLM-as-judge evaluation for the specialized QA agent.

Mirrors the eval.py pattern from the other project but integrated into
StemQA's benchmark pipeline.  For each generated test file, the judge scores
three dimensions on a 1-5 scale:

  specificity   — how precisely do the tests target the documented spec?
  coverage      — how many distinct bug categories do the tests probe?
  actionability — would a developer immediately understand which property
                  failed if a test breaks?

The judge sees: the function code, the docstring, and the generated tests.
It does NOT see whether the hidden tests pass — that's a separate metric.
"""

from __future__ import annotations

import json

from stem_agent.llm import call_json_model


JUDGE_SYSTEM_PROMPT = """\
You are an expert QA evaluator.  You will be shown a Python function and a
set of generated pytest tests.  Score the tests on three dimensions (1–5):

  specificity   (1=generic smoke tests, 5=tests precisely derived from the spec)
  coverage      (1=only happy path, 5=edges/side-effects/exceptions all covered)
  actionability (1=failure message reveals nothing, 5=failure immediately names
                 the broken contract)

Respond ONLY with valid JSON:
{"specificity": int, "coverage": int, "actionability": int, "reasoning": "one sentence"}
"""


def judge_tests(function_code: str, generated_tests: str) -> dict:
    """
    Ask the LLM judge to score a set of generated tests.

    Returns a dict with keys: specificity, coverage, actionability, reasoning.
    On parse failure, returns zeros with an error note.
    """
    user_prompt = (
        f"Function:\n{function_code}\n\n"
        f"Generated tests:\n{generated_tests}"
    )

    try:
        result = call_json_model(JUDGE_SYSTEM_PROMPT, user_prompt)
        return {
            "specificity":   int(result.get("specificity", 0)),
            "coverage":      int(result.get("coverage", 0)),
            "actionability": int(result.get("actionability", 0)),
            "reasoning":     result.get("reasoning", ""),
        }
    except Exception as exc:
        return {
            "specificity": 0,
            "coverage": 0,
            "actionability": 0,
            "reasoning": f"judge error: {exc}",
        }


def average_scores(scores: list[dict]) -> dict:
    """Average a list of judge score dicts across multiple problems."""
    if not scores:
        return {}
    dims = ("specificity", "coverage", "actionability")
    return {
        d: round(sum(s[d] for s in scores) / len(scores), 2)
        for d in dims
    }
