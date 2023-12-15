from typing import Any, Generator, Optional


class Expo(Generator):
    """
    Generator for exponential decay.
    """

    __slots__ = ("_base", "_factor", "_max_value", "_attempt", "_value")

    def __init__(self, *, max_value: Optional[int] = None, base: int = 2, factor: int = 1):
        """
        :param base: The mathematical base of the exponentiation operation
        :param factor: Factor to multiply the exponentiation by.
        :param max_value: The maximum value to yield. Once the value in the
        true exponential sequence exceeds this, the value
        of max_value will forever after be yielded.
        """
        self._base = base
        self._factor = factor
        self._max_value = max_value
        self._attempt = 0
        self._value: int = 0

    def send(self, _: Optional[Any]) -> int:
        self._value = self._factor * self._base**self._attempt
        if self._max_value is None or self._value < self._max_value:
            self._attempt += 1
            return self._value
        else:
            return self._max_value

    def throw(self, typ: Any, val: Any = None, tb: Any = None) -> Any:
        super().throw(typ, val, tb)
