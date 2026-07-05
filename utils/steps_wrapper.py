"""
Given/When/Then step grouping for Allure reporting, enforced against a
.feature file.

Design intent: every logical step of a test is a single code block where
the ACTION and its EXPECTATION live next to each other, with a
human-readable description supplied inline. @Gherkin(...) then verifies,
at runtime, that the exact sequence of given()/when()/then() calls made
by the test matches — word for word, in order, completely — the
Given/When/Then/And lines of the named scenario in the .feature file.

Three ways this can fail, all loud, all immediate:
  1. The scenario name doesn't exist in the .feature file (checked at
     import/collection time).
  2. A steps.given/when/then() call's text or type doesn't match the
     next expected line in the .feature file (checked as it happens).
  3. The test finishes but the .feature file had more lines left that
     were never executed (checked right after the test body returns).

Scenario Outline support:
  If the bound scenario has an Examples table, @Gherkin automatically
  applies pytest.mark.parametrize so each row becomes a separate test
  execution. Column names become pytest parameter names.
"""

from collections.abc import Callable
from contextlib import contextmanager
import functools
import inspect
from typing import TypeVar, cast

import allure
import pytest

from utils.gherkin_parser import GherkinStep, StepType, parse_feature_file
from utils.logger import get_logger

logger = get_logger()

F = TypeVar("F", bound=Callable)


class ScenarioStepMismatchError(AssertionError):
    """Raised when a test's given/when/then calls don't exactly match its bound .feature scenario."""


def Gherkin(feature_file: str, scenario_name: str) -> Callable[[F], F]:
    feature = parse_feature_file(feature_file)
    scenario = next((s for s in feature.scenarios if s.name.strip() == scenario_name.strip()), None)

    if scenario is None:
        available = [s.name for s in feature.scenarios]
        raise ValueError(
            f'Gherkin(): scenario "{scenario_name}" not found in features/{feature_file}. '
            f"Available scenarios: {available}. Fix the decorator argument or the .feature file — "
            f"this test cannot be collected until they agree."
        )
    if not scenario.steps:
        raise ValueError(
            f'Gherkin(): scenario "{scenario_name}" in features/{feature_file} has no Given/When/Then steps.'
        )

    def decorator(func: F) -> F:
        if "steps" not in inspect.signature(func).parameters:
            raise TypeError(
                f'@Gherkin requires a "steps: Steps" fixture parameter on {func.__name__}, so the scenario '
                f"can be verified step-by-step against features/{feature_file}. None was found."
            )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            steps_instance: Steps = kwargs["steps"]
            steps_instance._bind_scenario(f"{feature_file}::{scenario_name}", scenario.steps)
            result = func(*args, **kwargs)
            steps_instance._verify_complete()
            return result

        decorated = allure.story(scenario_name)(allure.feature(feature.name)(wrapper))

        if scenario.examples is not None:
            param_names = list(scenario.examples[0].keys())
            param_values = [tuple(row.values()) for row in scenario.examples]
            decorated = pytest.mark.parametrize(",".join(param_names), param_values)(decorated)

        return cast(F, decorated)

    return decorator


class Steps:
    def __init__(self) -> None:
        self._expected: list[GherkinStep] = []
        self._pointer: int = 0
        self._bound_to: str | None = None
        self._step_counter: int = 0

    def _bind_scenario(self, bound_to: str, expected_steps: list[GherkinStep]) -> None:
        self._expected = expected_steps
        self._pointer = 0
        self._bound_to = bound_to

    def _verify_complete(self) -> None:
        if self._pointer < len(self._expected):
            remaining = [f"{s.step_type.upper()} {s.text}" for s in self._expected[self._pointer :]]
            raise ScenarioStepMismatchError(
                f'Scenario "{self._bound_to}" is not fully covered by test code: {len(remaining)} step(s) '
                f"declared in the .feature file were never executed: {remaining}"
            )

    def _consume(self, step_type: StepType, description: str) -> None:
        if self._bound_to is None:
            return  # not bound to a scenario via @Gherkin — nothing to verify against

        if self._pointer >= len(self._expected):
            raise ScenarioStepMismatchError(
                f'Scenario "{self._bound_to}": extra {step_type.upper()} step "{description}" has no '
                f"corresponding line left in the .feature file."
            )

        expected = self._expected[self._pointer]
        if expected.step_type != step_type or expected.text != description:
            raise ScenarioStepMismatchError(
                f'Scenario "{self._bound_to}": step #{self._pointer + 1} does not match the .feature file.\n'
                f"  Expected: {expected.step_type.upper()} {expected.text!r}\n"
                f"  Got:      {step_type.upper()} {description!r}"
            )
        self._pointer += 1

    @contextmanager
    def given(self, description: str = "Setup"):
        self._consume("given", description)
        logger.info(f"▶ GIVEN: {description}")
        with allure.step(f"GIVEN: {description}"):
            yield self

    @contextmanager
    def step(self, description: str = ""):
        """Groups a When/Then pair (or related actions) under one auto-numbered Allure step.
        Not verified against the .feature file — it's a Python-only visual container, not a
        Gherkin line. The number comes from a counter on this Steps instance (one per test), so
        there is nothing for a human to type or keep in sync by hand."""
        self._step_counter += 1
        title = f"Step {self._step_counter}" if not description else f"Step {self._step_counter}: {description}"
        with allure.step(title):
            yield self

    @contextmanager
    def when(self, description: str):
        self._consume("when", description)
        logger.info(f"▶ WHEN: {description}")
        with allure.step(f"WHEN: {description}"):
            yield self

    @contextmanager
    def then(self, description: str):
        self._consume("then", description)
        logger.info(f"▶ THEN: {description}")
        with allure.step(f"THEN: {description}"):
            yield self
