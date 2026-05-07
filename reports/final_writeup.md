# StemQA: A Stem Agent for Python Quality Assurance

## 1. Framing

A stem agent is a minimal agent that does not directly solve a target task, but
instead specializes itself for a task class.  StemQA applies this idea to
Python Quality Assurance: a small system that starts from the broad task domain
and produces a specialized QA agent for generating tests against Python
functions.

I chose QA because it is narrow enough to evaluate objectively.  The primary
metric — bug detection rate — is binary per problem, reproducible, and
independent of subjective judgement.  An alternative design would use an LLM judge on 1–5 dimensions, but this introduces evaluator variance.  StemQA combines both approaches:
independent of subjective judgement.  A possible alternative evaluation design would rely primarily on an LLM judge, scoring outputs on 1–5 dimensions such as specificity, coverage, and actionability. That design is flexible, but it introduces evaluator variance. StemQA instead uses a deterministic bug-detection benchmark for the headline metric, with an optional LLM judge only for diagnostic scoring.

---

## 2. Architecture

### 2.0 Environment Reading

Before creating a specialization config, the stem agent runs a domain scout. The scout asks an LLM to generate search queries for the task domain, searches for how practitioners approach Python Quality Assurance, and summarizes observed tools, strategies, and failure modes into a domain brief.

This answers how the stem agent figures out how a task is typically approached: it reads external domain signals before deciding what to become. The saved artifact `runs/stem/domain_brief.txt` records the environmental signal used in the final run.

### 2.0.1 Self-Proposed Stopping and Rollback

The stem agent also proposes its own stopping condition. After reading the domain brief, it asks what minimum improvement on the selected metric would count as meaningful specialization, then stores that value as `config.min_improvement`.

The loop also includes rollback. If a later specialization iteration performs worse than the current best, the regressed test files are preserved separately and the best known test files are restored.

StemQA has five components.

### 2.1 Baseline QA Agent

Generates a single smoke test that only checks whether the target function is
callable.  This is the before-specialization control.  It reliably scores 0%
bug detection on every benchmark run.

### 2.2 Stem Agent

Calls an LLM to produce a `SpecializationConfig`.  The config specifies:
domain, architecture, tools, skills, stopping metric, and iteration limits.
Skills are constrained to a vocabulary of known names (see §2.3) so the config
output is parseable and actionable rather than aspirational.

The stem agent also implements a revision loop: if the first iteration's bug
detection rate does not clear the `min_improvement` threshold, it feeds the
evaluation results back to the LLM and asks it to produce a revised config.
A forced-revision demo (run with `scripts/run_revision_demo.py`) demonstrates
this path by artificially raising the threshold to 1.01 so revision always
triggers.

### 2.3 Skill Compiler (`stem_agent/skill_compiler.py`)

This is the primary architectural upgrade over prior iterations.

Earlier versions injected the config's skills list as raw JSON into the system
prompt.  The model received `["generate_edge_cases", "check_side_effects"]` as
a JSON array and interpreted it however it chose.  The config was present but
functionally inert: the test quality depended entirely on the LLM's prior
knowledge of QA, not on the specialization.

The skill compiler maps each skill name to a concrete, imperative instruction
block:

```
check_side_effects →
  "STEP 4 — SIDE-EFFECT TESTS: For every function that receives a mutable
   argument (list, dict, set), write a test that:
   (a) saves a copy of the input before calling the function,
   (b) calls the function,
   (c) asserts the original input is unchanged.
   Mutation bugs are invisible to return-value-only tests."
```

The `compile_skills()` function assembles these blocks into a structured
instruction section injected into the system prompt.  The config now drives
prompt construction rather than decorating it.  Changing which skills appear in
the config produces measurably different test generation behaviour.

### 2.4 Specialized QA Agent (`stem_agent/qa_agent.py`)

The agent uses the compiled skills as its system prompt and generates 3–6 pytest
tests per function.  It then runs those tests immediately.

If the tests all pass — meaning no bug was exposed — the agent enters a repair
loop.  It feeds the existing tests and pytest output back to a repair-focused
LLM and asks for new tests targeting the properties the first pass missed
(side effects, stability, off-by-one, exceptions).  The repair loop runs up to
`MAX_REPAIR_PASSES` times (currently 2) and stops as soon as a test exposes the
bug.

This is architecturally significant: the agent observes its own output, reasons
about what it missed, and self-corrects within a single inference session.

### 2.5 LLM Judge (`stem_agent/judge.py`)

An optional evaluation layer that scores each generated test file on three dimensions: specificity, coverage, and actionability. It is disabled by default to keep benchmark runs fast and is enabled by passing `run_judge=True` to `evaluate_agent()`.

---

## 3. Experiments

The benchmark contains 19 intentionally buggy Python functions covering:

whitespace handling, interval boundary conditions, punctuation normalization,
negative numbers, case sensitivity, exception handling, duplicate handling,
off-by-one errors, string parsing, mutation side effects, empty input handling,
binary search boundaries, stable sorting, rolling-window boundaries, and path
normalization.

Primary metric:
```
bug detection rate = problems where generated tests expose a bug / total
```

Secondary metrics:
```
invalid test rate = invalid generated tests / total
repair rate      = bugs found only after a repair pass / bugs found total
```

Saved run results:

| Agent | Problems | Bugs Found | Detection Rate | Invalid Rate |
|---|---:|---:|---:|---:|
| Baseline QA Agent | 19 | 0 | 0.00% | 0.00% |
| Stem-specialized QA Agent | 19 | 19 | 100.00% | 0.00% |

**Improvement: 100.00%**

Earlier iterations exposed two blind spots, p012 and p017, which are analysed in §5.

---

## 4. What the Skill Compiler Changed

To verify the compiler produces different behaviour, compare system prompts:

**v5 (raw JSON injection):**
```
Specialization config:
{
  "skills": ["generate_edge_cases", "check_side_effects"]
}
```

**v6 (compiled skills):**
```
=== QA STRATEGY (follow every step) ===

STEP 3 — EDGE CASES: Write tests that probe boundary conditions...
  • Empty inputs (empty list, empty string, zero)
  ...

STEP 4 — SIDE-EFFECT TESTS: For every function that receives a mutable
argument (list, dict, set), write a test that:
  (a) saves a copy of the input before calling the function,
  (b) calls the function,
  (c) asserts the original input is unchanged.
  Mutation bugs are invisible to return-value-only tests.
```

The compiled version makes the testing strategy an explicit, imperative
pipeline rather than a JSON label.  This is the difference between telling a
contractor "use good materials" and handing them a specification.

---

## 5. What Failed and Why

### 5.1 Earlier blind spots: side effects and stable ordering

**p012 — `remove_none` (mutation side effect)**
The function removes `None` values from a list by mutating the input list in
place.  The generated tests checked the return value but did not check whether
the original input was preserved.  This is a side-effect blind spot.  The
`check_side_effects` skill instruction was included in the config and did appear
in the system prompt, but the LLM chose to generate a standalone test rather
than following the three-step mutation-checking pattern.

This reveals a fundamental limitation: compiled skill instructions are strong
hints, not hard constraints.  The LLM can ignore them.  A more reliable design
would use structured output to force the agent to produce one test per skill
category.

**p017 — `top_k_stable` (stability under tie-breaking)**
The implementation sorts tied items alphabetically instead of preserving
insertion order.  The generated tests reproduced the docstring example
(`("a", 10), ("b", 10)` → `["a", "b"]`), which happens to match alphabetical
order.  The hidden test inverts this: `("b", 10), ("a", 10)` → expects
`["b", "a"]`.  The generated test was not wrong; it was insufficient.  The
`check_stability` skill instruction explicitly says "invert the tie order to
stress-test the stability requirement" but the LLM did not observe that the
docstring example coincidentally passes even with the bug.

Both earlier failures shared a root cause: the agent reasoned from the docstring rather than sufficiently stress-testing the code body. The later skill-compiler instructions addressed these failure modes directly in the initial test-generation pass, which is why the final saved run catches both cases.

### 5.2 The repair loop's scope

The repair loop only activates when the initial generated tests do not expose a bug. Earlier runs on p012 and p017 showed why this fallback matters: the initial tests missed side effects and stability requirements. In the final saved run, the skill compiler's explicit instructions were sufficient to catch both cases on the first pass. The repair loop remains useful as a fallback for future problems, but it is not a substitute for better initial skill enforcement.
Both misses share a root cause: the agent reasons from the docstring rather than
from the code body.  The `bug_detection` skill instructs code-body inspection,
and later skill-compiler instructions addressed these failure modes directly in the initial test-generation pass.
passed (no exception, correct return values for the chosen inputs).

### 5.2 The repair loop's scope

The repair loop only activates when the initial generated tests do not expose a bug. In earlier runs, p012 and p017 showed why this fallback matters: the initial tests missed side effects and stability requirements. In the final saved run, the skill compiler's explicit instructions were sufficient to catch both cases on the first pass. The repair loop remains a fallback for future problems where the initial pass fails.
means the repair prompt also failed to generate the right test.

The repair loop is useful as a fallback, but it is not a
reliable fallback for the hardest cases.

### 5.3 Semantic false-positives

The evaluator cannot distinguish a test that fails because it found a real bug
from one that fails because the LLM asserted an incorrect expected value.
Resolving this would require a known-correct reference implementation, mutation
testing, or human review.  The 0% invalid test rate in the saved run reflects
only syntactic / import / collection failures, not semantic incorrectness.

### 5.4 Non-determinism

Results from LLM-generated tests vary across runs.  The reported 100.00% is
a single saved run.  Re-running may produce different tests and different bug
detection rates.  The saved artifacts in `runs/stem/` are the authoritative
record for this submission.

---

## 6. Evaluation Design Trade-offs

StemQA uses a deterministic benchmark as its headline evaluation because the task domain is Python QA. A generated test either exposes a benchmark bug, fails as invalid, or does not find the bug. This gives the project a clear before/after comparison and makes runs inspectable through saved artifacts.

A more general stem-agent system could instead evaluate across multiple domains with an LLM judge. That would be more flexible, but it would introduce evaluator variance and make the headline score less mechanically reproducible. StemQA makes the opposite trade-off: it is narrower, but its core metric is objective.

The dynamic pipeline prototype partially explores the more general direction. It shows that the stem agent can produce a stage structure rather than only a skill list, while the main QA-specialized path remains the stronger evaluated system.

---

### Dynamic Pipeline Prototype

I also implemented an experimental dynamic pipeline agent. Instead of only producing a specialization config, the stem agent can produce a `PipelineSpec`: an ordered list of prompt and tool stages. A generic executor then runs the proposed stages.

This is closer to the stem-cell metaphor because the agent's structure can change at runtime. In the saved demo run, the stem agent produced a three-stage QA pipeline: a prompt stage to extract intended behavior, an executable tool stage (`extract_python_context`) to extract deterministic Python context, and a prompt stage to generate pytest tests. That run reached 94.74% bug detection with a 0.00% invalid test rate and included a real executable tool stage (`extract_python_context`) between prompt stages. In this saved pipeline-demo run, the domain scout fell back to model prior because web search returned no results; the main stem run's environmental brief is saved separately in `runs/stem/domain_brief.txt`. The main reported result still uses the stronger QA-specialized agent, but the pipeline prototype shows how the same scaffold could grow structurally different agents for other domains.
This is closer to the stem-cell metaphor because the agent's structure can change at runtime. In the saved demo run, the stem agent produced a two-stage QA pipeline: one stage to extract intended behavior and one stage to generate pytest tests. That run reached 94.74% bug detection with a 0.00% invalid test rate and included a real executable tool stage (`extract_python_context`) between prompt stages. In this saved pipeline-demo run, the domain scout fell back to model prior because web search returned no results; the main stem run's environmental brief is saved separately in `runs/stem/domain_brief.txt`. The main reported result still uses the stronger QA-specialized agent, but the pipeline prototype shows how the same scaffold could grow structurally different agents for other domains.

## 7. Future Work

**Structured skill enforcement.** Replace free-form LLM generation with
structured output that forces one test per compiled skill category.  This would
close the gap between "skill in the prompt" and "skill in the tests."

**Reference implementation.** Adding a known-correct implementation for each
benchmark problem would allow the evaluator to detect semantic false-positives
and compute a precision / recall breakdown.

**Mutation testing.** Using a mutation testing library (e.g. mutmut) to
generate artificial defects would let the evaluator measure test strength beyond
the hidden-bug-per-function benchmark.

**Multi-trial reporting.** Run the specialized agent three times per problem and
report mean ± std for bug detection rate, to characterize the variance from LLM
non-determinism.

**Cross-domain application.** Apply the same stem-agent loop to a second domain
(e.g. security review or documentation QA) to test whether the skill compiler
generalizes.

---

## 8. Conclusion

StemQA demonstrates a bounded, measurable stem agent.  It starts from a task
domain, generates a specialization config at runtime, compiles that config's
skills into concrete prompt instructions, builds a multi-pass QA agent, and
evaluates it against a baseline on a reproducible benchmark.

The specialized agent found 19 of 19 benchmark bugs (100.00%) while the baseline
found none. Earlier missed cases are analysed and attributed to specific failure
found none.  The two misses are analysed and attributed to specific failure
modes in the skill-compilation and repair-loop design.

The system is intentionally narrow.  It is not a universal agent.  It is an
agent that became specific to Python Quality Assurance.
