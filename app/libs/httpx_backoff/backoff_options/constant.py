import itertools
from typing import Any, Generator, Optional


class Constant(Generator):
    """
    Generator for constant intervals.
    """

    __slots__ = ("_interval",)

    def __init__(self, interval: int = 1):
        """
        :param interval: A constant interval to yield or an iterable of such values.
        """
        self._interval = itertools.repeat(interval)

    def send(self, _: Optional[Any]) -> int:
        return next(self._interval)

    def throw(self, typ: Any, val: Any = None, tb: Any = None) -> Any:
        super().throw(typ, val, tb)
