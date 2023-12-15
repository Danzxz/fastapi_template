from typing import Any, Generator, Optional


class Fibo(Generator):
    """
    Generator for fibonaccial decay.
    """

    __slots__ = ("_a", "_b", "_max_value")

    def __init__(self, max_value: Optional[int] = None):
        """
        :param max_value: The maximum value to yield. Once the value in the
         true fibonacci sequence exceeds this, the value
         of max_value will forever after be yielded.
        """
        self._max_value = max_value
        self._a = 1
        self._b = 1

    def send(self, _: Optional[Any] = None) -> int:
        if self._max_value is None or self._a < self._max_value:
            return_value = self._a
            self._a, self._b = self._b, self._a + self._b
            return return_value
        else:
            return self._max_value

    def throw(self, typ: Any, val: Any = None, tb: Any = None) -> Any:
        super().throw(typ, val, tb)
