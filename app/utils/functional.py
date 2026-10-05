"""Higher-order helpers."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def filter_fields(items: Iterable[T], condition: Callable[[T], bool]) -> list[T]:
    """Higher-order function: keep items for which ``condition`` is true."""
    return [item for item in items if condition(item)]
