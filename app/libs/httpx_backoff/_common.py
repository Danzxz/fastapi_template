from typing import Any, Optional, TypeVar

from httpx_backoff._typing import _BackoffGenerator, _Jitterer

T = TypeVar("T")


def _next_wait(
    wait: _BackoffGenerator,
    send_value: Any,
    elapsed: float,
    jitter: Optional[_Jitterer] = None,
    timeout: Optional[float | int] = None,
) -> float:
    value = wait.send(send_value)

    if jitter is not None:
        seconds = jitter(value)
    else:
        seconds = value

    # don't sleep longer than remaining allotted timeout
    if timeout is not None:
        seconds = min(seconds, timeout - elapsed)

    return seconds
