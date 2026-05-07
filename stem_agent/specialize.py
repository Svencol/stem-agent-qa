from stem_agent.domain_scout import scout_domain
from stem_agent.llm import call_json_model
from stem_agent.schemas import EvaluationSummary, SpecializationConfig
from stem_agent.skill_compiler import _SKILL_INSTRUCTIONS

_KNOWN_SKILLS = list(_SKILL_INSTRUCTIONS.keys())

_CONFIG_SCHEMA = """{
  "domain": "string",
  "architecture": "string",
  "tools": ["string"],
  "skills": ["string"],
  "stopping_metric": "string",
  "max_iterations": 3,
  "min_improvement": 0.15
}"""


def create_qa_specialization_config() -> tuple[SpecializationConfig, str]:
    """
    Scout the environment, then ask the stem agent to propose a config
    grounded in observed domain practice rather than model prior alone.

    Returns (config, domain_brief) so the brief can be saved as an artifact.
    """
    domain_brief = scout_domain("Python Quality Assurance")

    system_prompt = f"""\
You are a stem agent. You have just observed how Python Quality Assurance
is actually practiced. Use those observations to propose a specialization
config — not what you already know, but what the evidence suggests.

Return only JSON matching this schema:
{_CONFIG_SCHEMA}

Skills must come from this vocabulary:
{_KNOWN_SKILLS}

Ground your skill selection in the domain brief you received.
Include at least: read_docstring_specification, generate_edge_cases,
check_side_effects, bug_detection.
"""

    user_prompt = f"""\
Domain brief from environment observation:
{domain_brief}

Task: the specialized agent receives a Python function and docstring.
It generates pytest tests that expose likely bugs.

Propose a specialization config grounded in the observed practices above.
"""

    data = call_json_model(system_prompt, user_prompt)
    config = SpecializationConfig(**data)
    return config, domain_brief


def revise_qa_specialization_config(
    previous_config: SpecializationConfig,
    baseline_summary: EvaluationSummary,
    specialized_summary: EvaluationSummary,
) -> SpecializationConfig:
    """
    Ask the stem agent to revise its specialization config after evaluation.
    This creates an actual differentiation loop.
    """
    system_prompt = f"""\
You are a stem agent revising your own specialization strategy.
You receive your previous config and evaluation results.

Return an improved JSON config with the same schema:
{_CONFIG_SCHEMA}

Skills must come from this vocabulary:
{_KNOWN_SKILLS}
"""

    user_prompt = f"""\
Previous config:
{previous_config.model_dump_json(indent=2)}

Baseline evaluation:
{baseline_summary.model_dump_json(indent=2)}

Specialized evaluation:
{specialized_summary.model_dump_json(indent=2)}

Revise the specialization config. Focus on improving bug detection while keeping invalid tests low.
"""

    data = call_json_model(system_prompt, user_prompt)
    return SpecializationConfig(**data)


def propose_stopping_condition(domain_brief: str, stopping_metric: str) -> float:
    """
    Ask the stem agent to propose its own improvement threshold.

    The agent reasons about the domain difficulty and metric sensitivity
    to decide what delta constitutes meaningful specialization.
    Returns a float between 0.05 and 0.95.
    """
    system_prompt = (
        "You are a stem agent deciding when you are good enough to stop evolving. "
        "Given a domain brief and a metric name, propose a minimum improvement "
        "threshold (0.0–1.0) that would constitute meaningful specialization. "
        "Reason about: how hard the domain is, how noisy the metric is, "
        "and what improvement over a baseline is actually significant. "
        "Return only JSON: {\"min_improvement\": float, \"reasoning\": \"one sentence\"}"
    )
    user_prompt = (
        f"Domain brief:\n{domain_brief}\n\n"
        f"Stopping metric: {stopping_metric}\n\n"
        f"What minimum improvement on this metric means the agent has "
        f"meaningfully specialized?"
    )

    data = call_json_model(system_prompt, user_prompt)
    proposed = float(data.get("min_improvement", 0.15))
    reasoning = data.get("reasoning", "")

    clamped = max(0.05, min(0.95, proposed))
    print(f"  [STEM] Stopping condition: min_improvement={clamped:.2f} — {reasoning}")
    return clamped

def create_pipeline_spec(domain_brief: str, domain: str = "Python Quality Assurance"):
    """
    Ask the stem agent to design an executable pipeline for a task domain.

    Unlike SpecializationConfig, this describes stages and stage order.
    """
    from stem_agent.schemas import PipelineSpec

    system_prompt = """
You are a stem agent designing a pipeline for a specialized AI agent.

Given a domain brief, propose an ordered list of stages. Each stage is either:
- stage_type "prompt": an LLM instruction that processes the current input
- stage_type "tool": Python code for a function called run(input: str) -> str

Design the minimal pipeline that would let an agent handle this domain well.
Include 2 to 5 stages. You MUST include at least one tool stage that performs concrete computation, such as parsing, extraction, validation, or code execution.

For Python QA, include stages that:
- extract intended behavior from source/docstrings
- generate pytest tests
- optionally repair or strengthen tests

Return only JSON matching this shape:
{
  "domain": "string",
  "stages": [
    {
      "name": "string",
      "stage_type": "prompt or tool",
      "instruction": "string",
      "code": "string or null",
      "runs_on": "previous"
    }
  ],
  "stopping_metric": "string",
  "min_improvement": 0.15
}
"""

    user_prompt = f"""Domain: {domain}

Domain brief:
{domain_brief}

Design a dynamic pipeline for this domain.
"""

    data = call_json_model(system_prompt, user_prompt)
    data = _normalize_pipeline_data(data, domain)
    return PipelineSpec(**data)

def _normalize_pipeline_data(data: dict, domain: str) -> dict:
    """
    Normalize imperfect LLM pipeline specs.

    For Python QA, the final useful artifact must be pytest code. If the
    model proposes documentation/reporting stages after test generation, those
    stages are removed so the executor ends with pytest generation.
    """
    data.setdefault("domain", domain)
    data.setdefault("stopping_metric", "bug_detection_rate")
    data.setdefault("min_improvement", 0.15)

    stages = data.get("stages") or []

    for stage in stages:
        stage.setdefault("name", "unnamed_stage")
        stage.setdefault("stage_type", "prompt")

        if stage.get("instruction") is None:
            stage["instruction"] = f"Run stage {stage.get('name', 'unnamed')}."

        if stage.get("runs_on") is None:
            stage["runs_on"] = "previous"

    if _is_python_qa_domain(domain):
        stages = _force_pytest_final_stage(stages)
        stages = _ensure_execution_stage(stages)

    data["stages"] = stages
    return data


def _is_python_qa_domain(domain: str) -> bool:
    normalized = domain.lower()
    return "python" in normalized and ("qa" in normalized or "quality assurance" in normalized)



def _ensure_execution_stage(stages: list[dict]) -> list[dict]:
    """
    Ensure Python QA pipelines include at least one concrete tool stage.
    """
    has_tool = any(stage.get("stage_type") == "tool" for stage in stages)
    if has_tool:
        return stages

    execution_stage = {
        "name": "extract_python_context",
        "stage_type": "tool",
        "instruction": "Extract deterministic Python context before pytest generation.",
        "code": '''def run(input: str) -> str:
    lines = input.splitlines()
    def_lines = [line.strip() for line in lines if line.strip().startswith("def ")]
    imports = [line.strip() for line in lines if line.strip().startswith(("import ", "from "))]
    summary = [
        "Deterministic extraction:",
        "Function definitions: " + repr(def_lines),
        "Imports: " + repr(imports),
        "",
        "Original input:",
        input,
    ]
    return "\\n".join(summary)
''',
        "runs_on": "previous",
    }

    if stages:
        return stages[:1] + [execution_stage] + stages[1:]
    return [execution_stage]

def _force_pytest_final_stage(stages: list[dict]) -> list[dict]:
    """
    Keep stages up to pytest generation and remove later prose/report stages.
    If no pytest-generation stage exists, append one.
    """
    if not stages:
        return [_pytest_generation_stage()]

    kept = []
    found_generator = False

    for stage in stages:
        kept.append(stage)

        combined = f"{stage.get('name', '')} {stage.get('instruction', '')}".lower()
        is_prompt = stage.get("stage_type") == "prompt"
        mentions_tests = "test" in combined or "pytest" in combined
        mentions_generation = "generate" in combined or "write" in combined

        if is_prompt and mentions_tests and mentions_generation:
            found_generator = True
            break

    if found_generator:
        final = kept[-1]
        final["stage_type"] = "prompt"
        final["instruction"] = final.get("instruction", "") + """

Final output requirements:
- Return only valid pytest code.
- Do not include markdown.
- Do not include explanations.
- Import the target function from the module path provided in the input.
- Write tests that can be executed directly by pytest.
"""
        final["code"] = None
        final["runs_on"] = "previous"
        return kept

    stages.append(_pytest_generation_stage())
    return stages


def _pytest_generation_stage() -> dict:
    return {
        "name": "generate_pytest_tests",
        "stage_type": "prompt",
        "instruction": """Generate valid pytest tests from the provided Python source and module path.

Final output requirements:
- Return only valid pytest code.
- Do not include markdown.
- Do not include explanations.
- Import the target function from the module path provided in the input.
- Include normal cases and edge cases.
- Prefer boundary conditions, side effects, ordering/stability, exception behavior, and empty inputs.
""",
        "code": None,
        "runs_on": "previous",
    }

