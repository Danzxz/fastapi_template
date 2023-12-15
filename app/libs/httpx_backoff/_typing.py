from typing import Callable, Generator, Sequence, Type, TypeVar, Union

T = TypeVar("T")

_ExceptionGroup = Union[BaseException, Sequence[BaseException | Type[BaseException]]]
_BackoffGenerator = Generator[int, None, None]
_Jitterer = Callable[[float], float]
