import inspect
from dataclasses import fields as dataclass_fields
from functools import wraps
from typing import Callable

from allure_commons._allure import StepContext
from allure_commons.utils import represent


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


def allure_step(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args, **kwargs):
        __tracebackhide__ = True
        arg_spec = inspect.getfullargspec(func)
        params = {}
        args_dict = dict(zip(arg_spec.args, args))
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
    return inner
