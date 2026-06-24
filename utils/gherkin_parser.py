from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Literal, cast


@dataclass
class GherkinStep:
    step_type: Literal["given", "when", "then", "and"]
    step_number: int | None
    text: str


@dataclass
class GherkinScenario:
    name: str
    tags: list[str] = field(default_factory=list)
    steps: list[GherkinStep] = field(default_factory=list)


@dataclass
class GherkinFeature:
    name: str
    scenarios: list[GherkinScenario] = field(default_factory=list)


FEATURE_DIR = Path(__file__).parent.parent / "features"


def parse_feature_file(filepath: str) -> GherkinFeature:
    path = FEATURE_DIR / filepath
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {path}")

    content = path.read_text(encoding="utf-8")
    return _parse(content)


def _parse(content: str) -> GherkinFeature:
    lines = content.splitlines()
    feature = GherkinFeature(name="")
    current_scenario: GherkinScenario | None = None
    step_counter: int = 0

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("Feature:"):
            feature.name = stripped[len("Feature:") :].strip()
            continue

        if stripped.startswith("@"):
            if current_scenario:
                current_scenario.tags.append(stripped)
            continue

        if stripped.startswith("Scenario:"):
            current_scenario = GherkinScenario(name=stripped[len("Scenario:") :].strip())
            step_counter = 0
            feature.scenarios.append(current_scenario)
            continue

        if current_scenario is None:
            continue

        step = _parse_step(stripped, step_counter)
        if step:
            current_scenario.steps.append(step)
            if step.step_number is not None:
                step_counter = step.step_number

    return feature


def _parse_step(line: str, last_number: int) -> GherkinStep | None:
    for keyword in ("Given ", "When ", "Then ", "And "):
        if line.startswith(keyword):
            step_type = cast(Literal["given", "when", "then", "and"], keyword.strip().lower())
            rest = line[len(keyword) :]

            step_num_match = re.match(r"Step\s+(\d+):\s*(.*)", rest)
            if step_num_match:
                step_number = int(step_num_match.group(1))
                text = step_num_match.group(2)
            else:
                step_number = last_number + 1
                text = rest

            return GherkinStep(
                step_type=step_type,
                step_number=step_number,
                text=text,
            )

    return None


def get_scenario_by_name(feature_path: str, scenario_name: str) -> GherkinScenario:
    feature = parse_feature_file(feature_path)
    for scenario in feature.scenarios:
        if scenario.name.lower() == scenario_name.lower():
            return scenario
    available = [s.name for s in feature.scenarios]
    raise ValueError(f"Scenario '{scenario_name}' not found in '{feature_path}'. " f"Available: {available}")
