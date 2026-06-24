from collections.abc import Callable
from dataclasses import fields as dataclass_fields
from functools import wraps
import inspect
from typing import Any, TypeVar

from allure_commons._allure import StepContext
from allure_commons.utils import represent

F = TypeVar("F", bound=Callable)


def _extract_dto_params(args: tuple, kwargs: dict) -> dict:
    params = {}
    for arg in args:
        try:
            for f in dataclass_fields(arg):
                params[f.name] = represent(getattr(arg, f.name))
        except TypeError:
            pass
    for v in kwargs.values():
        try:
            for f in dataclass_fields(v):
                params[f.name] = represent(getattr(v, f.name))
        except TypeError:
            pass
    return params


def _func_parameters(func: Callable, *args: Any, **kwargs: Any) -> dict:
    arg_spec = inspect.getfullargspec(func)
    arg_order = list(arg_spec.args)
    args_dict = dict(zip(arg_spec.args, args, strict=False))

    if arg_spec.args and arg_spec.args[0] in ("cls", "self"):
        args_dict.pop(arg_spec.args[0], None)

    parameters: dict[str, Any] = {}
    if kwargs:
        parameters.update(kwargs)
    parameters.update(args_dict)

    sorted_items = sorted(
        ((k, represent(v)) for k, v in parameters.items() if k in arg_order),
        key=lambda x: arg_order.index(x[0]),
    )
    return dict(sorted_items)


def allure_step(func: F) -> F:
    @wraps(func)
    def inner(*args, **kwargs):
        __tracebackhide__ = True
        arg_spec = inspect.getfullargspec(func)
        params = {}
        args_dict = dict(zip(arg_spec.args, args, strict=False))
        if arg_spec.args and arg_spec.args[0] in ("cls", "self"):
            args_dict.pop(arg_spec.args[0], None)
        args_dict.pop("dto", None)
        for k, v in args_dict.items():
            params[k] = represent(v)
        params.update({k: represent(v) for k, v in kwargs.items()})
        params.update(_extract_dto_params(args, kwargs))
        title = func.__name__.replace("_", " ")
        with StepContext(title, params):
            return func(*args, **kwargs)

    return inner  # type: ignore[return-value]


class CheckStep:
    """Analog UICheckStep — wraps CommonChecker methods in allure steps."""

    def __init__(self, func: Callable) -> None:
        self.func = func

    def __get__(self, obj: Any, objtype: type | None = None) -> Callable:
        if obj is None:
            return self
        return lambda *args, **kwargs: self._call(obj, *args, **kwargs)

    def _call(self, obj: Any, *args: Any, **kwargs: Any) -> Any:
        params = _func_parameters(self.func, obj, *args, **kwargs)
        function_name = self.func.__name__.replace("_", " ")
        with StepContext(function_name, params):
            return self.func(obj, *args, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        params = _func_parameters(self.func, *args, **kwargs)
        function_name = self.func.__name__.replace("_", " ")
        with StepContext(function_name, params):
            return self.func(*args, **kwargs)
