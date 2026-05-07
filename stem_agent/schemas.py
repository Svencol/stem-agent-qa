from enum import Enum
from pydantic import BaseModel, Field


class BenchmarkProblem(BaseModel):
    id: str
    name: str
    problem_file: str
    hidden_test_file: str
    bug_type: str
    difficulty: str


class AgentResult(BaseModel):
    problem_id: str
    generated_test_file: str
    tests_ran: bool
    hidden_bug_found: bool
    invalid_tests: bool
    notes: str = ""


class EvaluationSummary(BaseModel):
    agent_name: str
    total_problems: int
    bugs_found: int
    invalid_test_count: int
    bug_detection_rate: float
    invalid_test_rate: float
    results: list[AgentResult] = Field(default_factory=list)


class SpecializationConfig(BaseModel):
    domain: str
    architecture: str
    tools: list[str]
    skills: list[str]
    stopping_metric: str
    max_iterations: int
    min_improvement: float


class StageType(str, Enum):
    prompt = "prompt"
    tool = "tool"


class PipelineStage(BaseModel):
    name: str
    stage_type: StageType
    instruction: str
    code: str | None = None
    runs_on: str = "previous"


class PipelineSpec(BaseModel):
    domain: str
    stages: list[PipelineStage]
    stopping_metric: str
    min_improvement: float = 0.15
