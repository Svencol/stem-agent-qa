"""
qa_agent.py
-----------
QA agents for StemQA.

BaselineQAAgent   — intentionally weak smoke-test generator (control).
SpecializedQAAgent — config-driven, skill-compiled, multi-pass QA agent.

Key upgrades over v5:
  1. compile_skills() turns the config's skills list into concrete imperative
     instructions rather than raw JSON injection.
  2. A repair loop runs the generated tests, feeds failures back to the LLM,
     and asks it to produce targeted fix tests — up to MAX_REPAIR_PASSES times.
  3. Returns a TestGenerationResult with per-pass metadata for the evaluator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from stem_agent.llm import call_text_model
from stem_agent.schemas import SpecializationConfig
from stem_agent.skill_compiler import compile_skills
from stem_agent.tools import read_text, run_pytest, write_text

MAX_REPAIR_PASSES = 2


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def module_path_from_file(problem_file: str) -> str:
    normalized = problem_file.replace("\\", "/")
    path = Path(normalized)
    without_suffix = path.with_suffix("")
    return ".".join(without_suffix.parts)


def _extract_function_name(code: str) -> str:
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def "):
            return line.split("def ")[1].split("(")[0]
    raise ValueError("No function definition found in source.")


def _clean_test_code(text: str) -> str:
    """
    Extract pytest code from LLM output.
    Handles raw code, fenced blocks, and explanatory text before a fence.
    """
    text = text.strip()

    if "```" in text:
        lines = text.splitlines()
        start = end = None

        for idx, line in enumerate(lines):
            if line.strip().startswith("```"):
                start = idx + 1
                break

        if start is not None:
            for idx in range(len(lines) - 1, start - 1, -1):
                if lines[idx].strip() == "```":
                    end = idx
                    break

            if end is not None:
                text = "\n".join(lines[start:end])
            else:
                text = "\n".join(lines[start:])

    return text.strip() + "\n"


# ---------------------------------------------------------------------------
# Baseline agent
# ---------------------------------------------------------------------------

class BaselineQAAgent:
    """
    Deliberately weak baseline: generates a smoke test that only checks
    whether the target function is callable.
    """

    name = "baseline_qa_agent"

    def generate_tests(self, problem_file: str, output_file: str) -> str:
        code = read_text(problem_file)
        module_path = module_path_from_file(problem_file)
        function_name = _extract_function_name(code)

        test_code = (
            f"from {module_path} import {function_name}\n\n\n"
            f"def test_smoke():\n"
            f"    assert {function_name} is not None\n"
        )

        write_text(output_file, test_code)
        return output_file


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class TestGenerationResult:
    """Metadata about what the specialized agent produced for one problem."""
    output_file: str
    repair_passes_used: int = 0
    final_passed: bool = False
    repair_history: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Specialized agent
# ---------------------------------------------------------------------------

class SpecializedQAAgent:
    """
    Config-driven QA agent with three upgrades over v5:

    1. Skill compilation   — compile_skills() maps the config's skills list to
                             concrete imperative instructions in the system
                             prompt.  The config now drives behaviour.

    2. Multi-pass repair   — after generating tests, if they all pass (no bug
                             exposed), the agent reads the output and generates
                             a targeted repair pass.  Repeats MAX_REPAIR_PASSES.

    3. Transparent result  — generate_tests_with_result() returns full metadata
                             including repair history.
    """

    name = "stem_specialized_qa_agent"

    def __init__(self, config: SpecializationConfig):
        self.config = config
        self._compiled_skills = compile_skills(config.skills)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate_tests(self, problem_file: str, output_file: str) -> str:
        """Entry point used by the evaluator (matches BaselineQAAgent interface)."""
        self.generate_tests_with_result(problem_file, output_file)
        return output_file

    def generate_tests_with_result(
        self, problem_file: str, output_file: str
    ) -> TestGenerationResult:
        """Full pipeline: initial generation + repair loop."""
        result = TestGenerationResult(output_file=output_file)

        code = read_text(problem_file)
        module_path = module_path_from_file(problem_file)
        function_name = _extract_function_name(code)

        # Pass 0: initial generation
        test_code = self._initial_generation(code, module_path, function_name)
        write_text(output_file, test_code)

        passed, pytest_output = run_pytest(output_file)
        result.final_passed = passed

        if passed:
            # All tests passed — bug not yet exposed.  Try repair passes.
            for repair_idx in range(MAX_REPAIR_PASSES):
                repair_code = self._repair_pass(
                    code, module_path, function_name,
                    existing_tests=test_code,
                    pytest_output=pytest_output,
                    pass_number=repair_idx + 1,
                )
                if repair_code is None:
                    break

                merged = test_code.rstrip() + "\n\n\n" + repair_code.strip() + "\n"
                try:
                    compile(merged, "<merged>", "exec")
                except SyntaxError:
                    result.repair_history.append(
                        f"pass {repair_idx + 1}: repair output failed compile check — skipped"
                    )
                    break
                write_text(output_file, merged)

                passed2, pytest_output2 = run_pytest(output_file)
                result.repair_passes_used += 1
                result.repair_history.append(
                    f"pass {repair_idx + 1}: "
                    + ("bug exposed" if not passed2 else "still passing")
                )

                if not passed2:
                    result.final_passed = False
                    test_code = merged
                    break

                test_code = merged
                pytest_output = pytest_output2

        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        base = (
            "You are a specialized Python QA agent.\n"
            "Generate only valid pytest code.\n"
            "Do not include markdown fences.\n"
            "Do not explain anything.\n\n"
        )
        if self._compiled_skills:
            base += "=== QA STRATEGY (follow every step) ===\n\n"
            base += self._compiled_skills
        return base

    def _initial_generation(
        self, code: str, module_path: str, function_name: str
    ) -> str:
        system_prompt = self._build_system_prompt()

        user_prompt = (
            f"Problem file module: {module_path}\n"
            f"Target function: {function_name}\n\n"
            f"Function source:\n{code}\n\n"
            f"Requirements:\n"
            f"- Import using: from {module_path} import {function_name}\n"
            f"- Write 3 to 6 tests.\n"
            f"- Every test function name must start with 'test_'.\n"
            f"- Include normal cases, edge cases, and side-effect / stability "
            f"checks where the spec warrants them.\n"
            f"- Tests must be syntactically valid pytest.\n"
            f"- Do not include markdown.\n"
        )

        raw = call_text_model(system_prompt, user_prompt)
        return _clean_test_code(raw)

    def _repair_pass(
        self,
        code: str,
        module_path: str,
        function_name: str,
        existing_tests: str,
        pytest_output: str,
        pass_number: int,
    ) -> str | None:
        """
        Generate additional tests targeting properties the first pass missed.
        Returns None if the LLM signals SKIP (tests are already exhaustive).
        """
        system_prompt = (
            "You are a Python QA repair agent.\n"
            "You will be shown a function and existing tests that ALL PASSED "
            "(meaning no bug was exposed yet).\n\n"
            "Your job: write NEW tests probing properties the existing tests "
            "did NOT cover.  Focus on:\n"
            "  - Side effects: does the function mutate its input?\n"
            "  - Stability: does tie-breaking preserve insertion order?\n"
            "  - Off-by-one at exact boundary values\n"
            "  - Exception contract: does it raise when the spec says it should?\n"
            "  - Inverted documented examples (swap argument order or polarity)\n\n"
            "If the existing tests are already exhaustive, respond with exactly: SKIP\n\n"
            "Otherwise, output ONLY valid pytest functions — no imports, no "
            "markdown.  They will be appended to the existing test file.\n"
        )

        user_prompt = (
            f"Repair pass {pass_number}\n\n"
            f"Function source:\n{code}\n\n"
            f"Existing tests (all passed — bug not yet found):\n{existing_tests}\n\n"
            f"Pytest output:\n{pytest_output}\n\n"
            f"Write additional tests targeting the gaps above."
        )

        raw = call_text_model(system_prompt, user_prompt).strip()

        if raw.upper().startswith("SKIP") or len(raw) < 20:
            return None

        return _clean_test_code(raw)
