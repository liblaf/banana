from collections.abc import Callable
from typing import Any, TypeVar

import glom

_T = TypeVar("_T")


def assign_if_missing(
    obj: _T, path: str, val: Any, missing: Callable | None = dict
) -> _T:
    try:
        glom.glom(obj, path)
    except glom.PathAccessError:
        return glom.assign(obj, path, val, missing=missing)
    else:
        return obj
