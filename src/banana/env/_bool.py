import functools
import os
from typing import overload

import pydantic


@overload
def get_bool(key: str) -> bool | None: ...
@overload
def get_bool(key: str, default: bool) -> bool: ...  # noqa: FBT001
def get_bool(key: str, default: bool | None = None) -> bool | None:
    if val := os.getenv(key):
        return adapter(bool).validate_strings(val)
    return default


@functools.cache
def adapter(t: type) -> pydantic.TypeAdapter:
    return pydantic.TypeAdapter(t)
