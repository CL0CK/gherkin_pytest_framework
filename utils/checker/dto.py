from dataclasses import dataclass

from utils.checker.mixins import (
    PresenceMixin,
    ValueColorMixin,
    ValueFontMixin,
    ValueTextMixin,
)


@dataclass
class ElementDTO(PresenceMixin):
    pass


@dataclass
class TextElementDTO(ValueTextMixin, ValueColorMixin, ValueFontMixin, ElementDTO):
    contains_text: bool = False


@dataclass
class ButtonElementDTO(ValueTextMixin, ValueColorMixin, ElementDTO):
    is_enabled: bool = True


@dataclass
class ImageElementDTO(ElementDTO):
    src_contains: str | None = None
    alt_text: str | None = None


@dataclass
class CountDTO:
    expected: int
    timeout: int = 5000
