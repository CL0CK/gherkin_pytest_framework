class Element:
    def __init__(self, selector: str, name: str = "") -> None:
        self.selector = selector
        self._name = name

    @property
    def name(self) -> str:
        return self._name or self.selector

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Element({self.selector!r}, name={self._name!r})"
