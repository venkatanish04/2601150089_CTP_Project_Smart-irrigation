"""Performance-measurement decorator."""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger(__name__)
TIMINGS: dict[str, list[float]] = {}


def measure_time(func: Callable[P, R]) -> Callable[P, R]:
    """Record the wall-clock time of every call in TIMINGS and log it."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        TIMINGS.setdefault(func.__name__, []).append(elapsed)
        logger.debug("%s took %.6fs", func.__name__, elapsed)
        return result

    return wrapper
