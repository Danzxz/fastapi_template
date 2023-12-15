from typing import Any, Callable, Generator


class Runtime(Generator):
    """
    Generator that is based on parsing the return func or thrown
    exception to the decorated method
    """

    __slots__ = ("_func",)

    def __init__(self, func: Callable[[Any], int]):
        self._func = func

    def send(self, value: Any) -> int:
        return self._func(value)

    def throw(self, typ: Any, val: Any = None, tb: Any = None) -> Any:
        super().throw(typ, val, tb)
