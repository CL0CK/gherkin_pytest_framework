from collections.abc import Callable
from contextlib import contextmanager
from functools import wraps
from typing import Any

import allure

from utils.checker.context import CheckerContext
from utils.gherkin_parser import (
    GherkinScenario,
    GherkinStep,
    get_scenario_by_name,
    parse_feature_file,
)
from utils.logger import get_logger

logger = get_logger()


class Steps:
    def __init__(self, scenario: GherkinScenario | None = None):
        self._scenario = scenario
        self._current_step: GherkinStep | None = None
        self._step_index: int = 0
        self._given_index: int = 0

    @contextmanager
    def given(self):
        step = self._get_given_step()
        text = step.text if step else "Setup"
        CheckerContext.set(phase="given", text=text)
        logger.info(f"▶ GIVEN: - {text}")
        with allure.step(f"GIVEN: {text}"):
            self._current_step = step
            self._given_index += 1
            yield self

    @contextmanager
    def step(self, number: int):
        with allure.step(f"Step {number}"):
            self._step_index = number
            yield self

    @contextmanager
    def when(self):
        step = self._find_step_for_number("when", self._step_index)
        text = step.text if step else "Action"
        CheckerContext.set(step_number=self._step_index, phase="when", text=text)
        logger.info(f"▶ WHEN #{self._step_index}: - {text}")
        with allure.step(f"WHEN: {text}"):
            self._current_step = step
            yield self

    @contextmanager
    def then(self):
        step = self._find_step_for_number("then", self._step_index)
        text = step.text if step else "Assertion"
        CheckerContext.set(step_number=self._step_index, phase="then", text=text)
        logger.info(f"▶ THEN #{self._step_index}: - {text}")
        with allure.step(f"THEN: {text}"):
            self._current_step = step
            yield self

    def _get_given_step(self) -> GherkinStep | None:
        if self._scenario:
            given_steps = [s for s in self._scenario.steps if s.step_type == "given"]
            if self._given_index < len(given_steps):
                return given_steps[self._given_index]
        return None

    def _find_step_for_number(self, step_type: str, number: int) -> GherkinStep | None:
        if self._scenario:
            for s in self._scenario.steps:
                if s.step_type == step_type and s.step_number == number:
                    return s
        return None


def Gherkin(feature_path: str, scenario_name: str | None = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            scenario = None
            feature_name = None

            try:
                feature = parse_feature_file(feature_path)
                feature_name = feature.name
            except Exception as e:
                logger.error(f"Failed to parse feature {feature_path}: {e}")

            try:
                if scenario_name:
                    scenario = get_scenario_by_name(feature_path, scenario_name)
            except Exception as e:
                logger.error(f"Failed to find scenario: {e}")

            steps_instance = kwargs.get("steps")
            if steps_instance and scenario:
                steps_instance._scenario = scenario

            allure.label("feature", feature_name or "Unknown")
            allure.label("scenario", scenario.name if scenario else "Unknown")

            CheckerContext.clear()
            return func(*args, **kwargs)

        wrapper._gherkin_feature = feature_path  # type: ignore[attr-defined]
        wrapper._gherkin_scenario = scenario_name  # type: ignore[attr-defined]
        return wrapper

    return decorator
