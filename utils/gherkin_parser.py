"""
.feature file reader with full step-level parsing.

The Gherkin decorator in utils/steps_wrapper.py uses this to build an
ordered contract of (step_type, text) pairs for a scenario. Steps.given/
when/then must be called with EXACTLY this text, in EXACTLY this order,
or the test fails immediately with a clear mismatch error. There is no
fuzzy matching and no silent fallback: either the code fully and exactly
describes the scenario, or the test errors out.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

FEATURE_DIR = Path(__file__).parent.parent / "features"

StepType = Literal["given", "when", "then"]

_KEYWORDS = ("Given ", "When ", "Then ", "And ", "But ")


@dataclass
class GherkinStep:
    step_type: StepType
    text: str


@dataclass
class GherkinScenario:
    name: str
    tags: list[str] = field(default_factory=list)
    steps: list[GherkinStep] = field(default_factory=list)
    examples: list[dict[str, str]] | None = None


@dataclass
class GherkinFeature:
    name: str
    scenarios: list[GherkinScenario] = field(default_factory=list)


def parse_feature_file(filename: str) -> GherkinFeature:
    path = FEATURE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {path}")

    feature = GherkinFeature(name="")
    current: GherkinScenario | None = None
    pending_tags: list[str] = []
    last_type: StepType | None = None
    parsing_examples = False
    example_headers: list[str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("Feature:"):
            feature.name = line.removeprefix("Feature:").strip()
        elif line.startswith("@"):
            pending_tags.extend(line.split())
        elif line.startswith("Scenario Outline:") or line.startswith("Scenario:"):
            prefix = "Scenario Outline:" if line.startswith("Scenario Outline:") else "Scenario:"
            current = GherkinScenario(name=line.removeprefix(prefix).strip(), tags=pending_tags)
            feature.scenarios.append(current)
            pending_tags = []
            last_type = None
            parsing_examples = False
            example_headers = None
        elif current is not None and line.startswith("Examples:"):
            parsing_examples = True
            example_headers = None
        elif current is not None and parsing_examples and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if example_headers is None:
                example_headers = cells
            else:
                row = dict(zip(example_headers, cells, strict=True))
                if current.examples is None:
                    current.examples = []
                current.examples.append(row)
        elif current is not None:
            parsing_examples = False
            example_headers = None
            for keyword in _KEYWORDS:
                if line.startswith(keyword):
                    text = line[len(keyword) :].strip()
                    if keyword in ("And ", "But "):
                        if last_type is None:
                            raise ValueError(
                                f'"{keyword.strip()}" step used before any Given/When/Then in scenario '
                                f'"{current.name}" (features/{filename}).'
                            )
                        step_type: StepType = last_type
                    else:
                        step_type = keyword.strip().lower()  # type: ignore[assignment]
                    current.steps.append(GherkinStep(step_type=step_type, text=text))
                    last_type = step_type
                    break

    return feature


def get_scenario_by_name(filename: str, scenario_name: str) -> GherkinScenario:
    feature = parse_feature_file(filename)
    for scenario in feature.scenarios:
        if scenario.name.strip() == scenario_name.strip():
            return scenario
    available = [s.name for s in feature.scenarios]
    raise ValueError(f'Scenario "{scenario_name}" not found in features/{filename}. Available scenarios: {available}')
