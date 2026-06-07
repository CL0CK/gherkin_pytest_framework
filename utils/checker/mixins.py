from dataclasses import dataclass


@dataclass
class ValueTextMixin:
    value_text: str | None = None
    expected_fail_value_text: str | None = None
    expected_fail_value_text_task: str | None = None
    expected_fail_all_text_values: bool = False


@dataclass
class ValueColorMixin:
    expected_color: str | None = None
    with_color_check: bool = False


@dataclass
class ValueFontMixin:
    expected_font_family: str | None = None
    expected_font_size: str | None = None
    with_font_check: bool = False


@dataclass
class PresenceMixin:
    is_visible: bool = True
    is_hidden: bool = False
    with_waiting: bool = True
    timeout: int = 5000
