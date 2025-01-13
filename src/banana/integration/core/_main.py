import functools
import inspect
from collections.abc import Callable
from typing import ParamSpec, TypeVar

import comet_ml as comet

import banana as bn

_P = ParamSpec("_P")
_T = TypeVar("_T")


def main(
    banana: bn.Banana | None = None,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def wrapper(fn: Callable[_P, _T]) -> Callable[_P, _T]:
        @functools.wraps(fn)
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            nonlocal banana
            if banana is None:
                banana = bn.Banana()
            banana.start()
            sig: inspect.Signature = inspect.signature(fn)
            bound_args: inspect.BoundArguments = sig.bind(*args, **kwargs)
            if len(bound_args.arguments) == 1:
                exp: comet.CometExperiment = comet.get_running_experiment()  # pyright: ignore[reportAssignmentType]
                exp.log_parameters(next(iter(bound_args.arguments.values())))
            elif len(bound_args.arguments) > 1:
                exp: comet.CometExperiment = comet.get_running_experiment()  # pyright: ignore[reportAssignmentType]
                exp.log_parameters(bound_args.arguments)
            result: _T = fn(*args, **kwargs)
            banana.end()
            return result

        return wrapped

    return wrapper
