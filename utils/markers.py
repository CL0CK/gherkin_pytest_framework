import pytest
from _pytest.mark import MarkDecorator

smoke: MarkDecorator = pytest.mark.smoke
regression: MarkDecorator = pytest.mark.regression
critical: MarkDecorator = pytest.mark.critical
