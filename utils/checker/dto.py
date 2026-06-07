from dataclasses import dataclass
from utils.checker.mixins import (
    ValueTextMixin,
    ValueColorMixin,
    ValueFontMixin,
    PresenceMixin,
)


@dataclass
class TextElementDTO(ValueTextMixin, ValueColorMixin, ValueFontMixin, PresenceMixin):
    contains_text: bool = False


@dataclass
class ButtonElementDTO(ValueTextMixin, ValueColorMixin, PresenceMixin):
    is_enabled: bool = True


@dataclass
class ImageElementDTO(PresenceMixin):
    src_contains: str | None = None
    alt_text: str | None = None


@dataclass
class ElementDTO(PresenceMixin):
    pass


@dataclass
class CountDTO:
    expected: int
    timeout: int = 5000
