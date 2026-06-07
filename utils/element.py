from dataclasses import dataclass


@dataclass
class Element:
    selector: str
    _name: str = ""

    @property
    def name(self) -> str:
        return self._name or self.selector

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Element({self.selector!r}, name={self._name!r})"
