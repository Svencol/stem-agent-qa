# StemQA

StemQA is a stem-agent prototype that specializes itself into a Python Quality Assurance agent.

The starting agent is intentionally minimal. Given the task class **Python QA**, it asks an LLM to produce a task-specific specialization configuration. That configuration defines the architecture, tools, skills, metric, and stopping rule for a specialized QA agent.

The specialized agent then uses that generated configuration to produce pytest tests for buggy Python functions. The result is evaluated against a weak baseline agent.

## Why QA?

Quality Assurance is narrow enough to evaluate objectively but rich enough to require meaningful specialization.

A useful QA agent needs to:

- read a function and its docstring,
- infer expected behavior,
- generate normal cases,
- generate edge cases,
- run tests,
- distinguish real bug exposure from invalid tests.

This makes QA a good domain for testing whether a stem agent actually becomes task-specific.

## Architecture

StemQA has four main parts:

1. **Baseline QA Agent**  
   A weak comparison agent that generates shallow smoke tests.

2. **Stem Agent**  
   Uses an LLM at runtime to create a `SpecializationConfig`.

3. **Specialized QA Agent**  
   Uses the generated config to condition an LLM-based pytest generator.

4. **Evaluator**  
   Runs generated tests and measures bug detection rate and invalid test rate.

## Differentiation Process

The stem agent follows this process:

1. Receive the task domain: Python Quality Assurance.
2. Ask an LLM to propose a specialization configuration.
3. Save the generated configuration as an artifact.
4. Build a specialized QA agent from that configuration.
5. Generate tests for each benchmark problem.
6. Run the tests with pytest.
7. Compare specialized performance against the baseline.
8. Stop once the improvement threshold is met, or revise the configuration.

The specialization config is not just saved for display. It is passed into the specialized QA agent and directly affects the prompt used to generate tests.

## Setup

Clone the repository:

```bash
git clone https://github.com/Svencol/stem-agent-qa.git

cd stem-agent-qa
```

Install dependencies:

```bash
python -m pip install -e .
```

Create a `.env` file:

```bash
cp .env.example .env
```

Then add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

## Run

Run the baseline agent:

```bash
python scripts/run_baseline.py
```

Run the specialized agent:

```bash
python scripts/run_specialized.py
```

Run the full stem-agent flow:

```bash
python scripts/run_stem_agent.py
```

Generate the results table:

```bash
python scripts/make_report_tables.py
```

Run project tests:

```bash
python -m pytest tests -q
```

## Evaluation

The benchmark contains 19 intentionally buggy Python functions covering multiple bug categories:

- whitespace handling
- interval boundary conditions
- punctuation normalization
- negative numbers
- case sensitivity
- exception handling
- duplicate handling
- off-by-one errors
- string parsing
- mutation side effects
- empty input handling
- binary search boundaries
- stable sorting
- rolling-window boundaries
- path normalization and stack-underflow boundaries

The primary metric is:

```text
bug detection rate = bugs found / total benchmark problems
```

The secondary metric is:

```text
invalid test rate = invalid generated tests / total benchmark problems
```

Invalid tests include syntax errors, import errors, name errors, or pytest collection errors.

## Current Result

The saved run artifacts report:

| Agent | Total Problems | Bugs Found | Bug Detection Rate | Invalid Test Rate |
|---|---:|---:|---:|---:|
| Baseline QA Agent | 19 | 0 | 0.00% | 0.00% |
| Stem-specialized QA Agent | 19 | 19 | 100.00% | 0.00% |

Improvement: **100.00%**

Because the specialized agent uses an LLM, exact results may vary across runs. The saved artifacts in `runs/stem/` record the evaluated run used in the report.

## Important Note About Hidden Tests

The tests in `benchmarks/hidden_tests/` are expected to fail because the benchmark functions are intentionally buggy.

This command is expected to produce failures:

```bash
python -m pytest benchmarks/hidden_tests -q
```

The project infrastructure tests are in `tests/` and should pass:

```bash
python -m pytest tests -q
```

## Repository Layout

```text
stem-agent-qa/
├── benchmarks/
│   ├── problems/
│   ├── hidden_tests/
│   └── metadata.json
├── reports/
│   ├── final_writeup.md
│   └── results_table.md
├── runs/
│   └── stem/
├── scripts/
│   ├── make_report_tables.py
│   ├── run_baseline.py
│   ├── run_specialized.py
│   └── run_stem_agent.py
├── stem_agent/
│   ├── evaluator.py
│   ├── llm.py
│   ├── qa_agent.py
│   ├── schemas.py
│   ├── specialize.py
│   └── tools.py
└── tests/
```

## Key Files

- `stem_agent/specialize.py`  
  LLM-backed stem agent that creates and revises specialization configs.

- `stem_agent/qa_agent.py`  
  Baseline and config-driven specialized QA agents.

- `stem_agent/evaluator.py`  
  Evaluation harness for generated tests.

- `benchmarks/metadata.json`  
  Benchmark problem registry.

- `reports/final_writeup.md`  
  Short project write-up.

## Limitations

The benchmark is still small and synthetic. The current system tests whether specialization helps on compact Python functions, not large real-world repositories.

The specialized agent also depends on LLM behavior, so results may vary across runs. For this reason, the repository stores run artifacts for reproducibility.

## Future Work

Possible extensions:

- add mutation testing
- add more benchmark problems
- evaluate on real open-source bugs
- add multiple task domains
- compare different specialization strategies
- add confidence intervals over repeated LLM runs

## Write-up

See:

```text
reports/final_writeup.md
```
cd stem-agent-qa
