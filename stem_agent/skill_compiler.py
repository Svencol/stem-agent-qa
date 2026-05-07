"""
skill_compiler.py
-----------------
Translates a SpecializationConfig's skills list into concrete, structured
prompt instructions that are injected into the QA agent's system prompt.

This is the missing coupling layer from v5: instead of dumping raw JSON into
the prompt and hoping the model interprets it, we compile each skill into an
explicit, imperative instruction block.  The specialization config now
*drives* behavior rather than merely decorating it.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Static skill → instruction mapping
# ---------------------------------------------------------------------------
# Each key is a canonical skill name the LLM might produce.
# Each value is the concrete instruction block injected into the system prompt.
# Partial matches (startswith / substring) are handled by _resolve below.

_SKILL_INSTRUCTIONS: dict[str, str] = {
    "read_docstring_specification": (
        "STEP 1 — READ THE SPEC: Before writing any test, read the function's "
        "docstring carefully. Extract: (a) the return type, (b) every stated "
        "invariant, (c) every documented example. Your tests must be grounded "
        "in these — never invent behaviour the spec does not claim."
    ),
    "generate_normal_cases": (
        "STEP 2 — NORMAL CASES: Write at least one test that exercises the "
        "documented happy-path examples verbatim. If the docstring gives "
        "concrete examples (e.g. f([1,2], 3) → 5), include them as-is so "
        "a correct implementation always passes."
    ),
    "generate_edge_cases": (
        "STEP 3 — EDGE CASES: Write tests that probe boundary conditions the "
        "implementation is likely to handle incorrectly:\n"
        "  • Empty inputs (empty list, empty string, zero)\n"
        "  • Single-element inputs\n"
        "  • Maximum / minimum values\n"
        "  • Inputs that differ by exactly one from a boundary\n"
        "  • Duplicate values if the function processes collections"
    ),
    "check_side_effects": (
        "STEP 4 — SIDE-EFFECT TESTS: For every function that receives a mutable "
        "argument (list, dict, set), write a test that:\n"
        "  (a) saves a copy of the input before calling the function,\n"
        "  (b) calls the function,\n"
        "  (c) asserts the original input is unchanged.\n"
        "Mutation bugs are invisible to return-value-only tests."
    ),
    "check_stability": (
        "STEP 4 — STABILITY / ORDER TESTS: If the function's docstring makes "
        "any claim about preserving order, tie-breaking, or stability, write a "
        "test that *inverts* the documented example so the tie-breaking order "
        "is the opposite of alphabetical. A correct implementation preserves "
        "insertion order; a buggy one breaks it only when order ≠ alphabetical."
    ),
    "generate_metamorphic_tests": (
        "STEP 5 — METAMORPHIC TESTS: Write at least one test that exploits a "
        "known relationship between inputs and outputs:\n"
        "  • Commutativity: f(a, b) == f(b, a) if applicable\n"
        "  • Idempotence: f(f(x)) == f(x) if applicable\n"
        "  • Inverse: decode(encode(x)) == x if applicable\n"
        "  • Scaling: f(2*x) relates predictably to f(x)"
    ),
    "check_exception_handling": (
        "STEP 5 — EXCEPTION TESTS: If the docstring documents that the function "
        "raises an exception under specific conditions (e.g. ValueError for "
        "negative input), write a pytest.raises test for each such condition. "
        "Also test the boundary: the value just inside the valid range must "
        "NOT raise."
    ),
    "execute_tests": (
        "OUTPUT RULE: Produce only valid, runnable pytest code. "
        "No markdown fences. No explanatory prose. "
        "Every test function must start with 'test_'. "
        "All imports must appear at the top of the file."
    ),
    "bug_detection": (
        "BUG-HUNTING MINDSET: Your goal is not to document correct behaviour — "
        "it is to expose the specific defect hiding in this implementation. "
        "Read the code body, not just the docstring. Look for:\n"
        "  • Off-by-one in loop bounds or slice indices\n"
        "  • Wrong initial value (e.g. max starting at 0 instead of -inf)\n"
        "  • Missing .strip() / .lower() / type conversion\n"
        "  • Mutation of the input argument\n"
        "  • Stability assumption violated by sorting key\n"
        "  • Wrong operator (> vs >=, + vs -, * vs **)\n"
        "Write the test that will catch the actual bug you observe."
    ),
    "code_analysis": (
        "CODE ANALYSIS: Before writing tests, inspect the function body for "
        "suspicious patterns: hardcoded initial values, asymmetric comparisons, "
        "missing edge-case guards, and side-effecting mutations. Let what you "
        "find in the code guide which edge cases to prioritise."
    ),
    "test_optimization": (
        "TEST QUALITY: Prefer 3 precise, targeted tests over 5 generic ones. "
        "Each test should be independently falsifiable — do not bundle multiple "
        "assertions that test the same property into one test function."
    ),
}

# Fallback for skills not in the table — produces a minimal instruction.
_FALLBACK_TEMPLATE = (
    "Apply skill '{skill}': incorporate it into your test generation "
    "strategy as appropriate for the function under test."
)


def _resolve(skill: str) -> str:
    """Return the instruction for a skill name, using prefix/substring matching."""
    key = skill.lower().strip().replace(" ", "_").replace("-", "_")
    if key in _SKILL_INSTRUCTIONS:
        return _SKILL_INSTRUCTIONS[key]
    # Try prefix match
    for canonical, instruction in _SKILL_INSTRUCTIONS.items():
        if key.startswith(canonical) or canonical.startswith(key):
            return instruction
    # Try substring match
    for canonical, instruction in _SKILL_INSTRUCTIONS.items():
        if key in canonical or canonical in key:
            return instruction
    return _FALLBACK_TEMPLATE.format(skill=skill)


def compile_skills(skills: list[str]) -> str:
    """
    Compile a list of skill names into a structured instruction block.

    Returns a multi-line string ready to be injected into a system prompt.
    The output is ordered so spec-reading comes first, output rules last,
    and bug-hunting mindset is always included regardless of the skills list.
    """
    if not skills:
        return ""

    # Ensure bug_detection is always present — it's the core QA mandate
    augmented = list(skills)
    if not any("bug" in s.lower() or "detection" in s.lower() for s in augmented):
        augmented.append("bug_detection")

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for s in augmented:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    instructions = [_resolve(s) for s in unique]
    return "\n\n".join(instructions)
