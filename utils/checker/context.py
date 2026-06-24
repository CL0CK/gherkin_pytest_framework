from dataclasses import dataclass


@dataclass
class _ContextState:
    step_number: int | None = None
    phase: str | None = None  # "given" | "when" | "then"
    text: str | None = None


class CheckerContext:
    _state: _ContextState = _ContextState()

    @classmethod
    def set(cls, step_number: int | None = None, phase: str | None = None, text: str | None = None):
        cls._state.step_number = step_number
        cls._state.phase = phase
        cls._state.text = text

    @classmethod
    def clear(cls):
        cls._state = _ContextState()

    @classmethod
    def label(cls) -> str:
        if cls._state.phase == "given":
            return "▶ GIVEN"
        if cls._state.phase == "when":
            return f"▶ WHEN #{cls._state.step_number}"
        if cls._state.phase == "then":
            return f"▶ THEN #{cls._state.step_number}"
        return ""

    @classmethod
    def text(cls) -> str | None:
        return cls._state.text
