import random


def use_equal_jitter(value: float) -> float:
    """Jitter the func across the equal range (func/2 to random(0 to func/2)).
    This corresponds to the "Equal Jitter" algorithm specified in the
    AWS blog's post on the performance of various jitter algorithms.
    https://www.awsarchitectureblog.com/2015/03/backoff.html

    :param value: The unadulterated backoff func.
    :return: sum of func and random
    """
    return value / 2 + random.uniform(0, value / 2)


def use_full_jitter(value: float) -> float:
    """
    Jitter the func across the full range (0 to func).
    This corresponds to the "Full Jitter" algorithm specified in the
    AWS blog's post on the performance of various jitter algorithms.
    https://www.awsarchitectureblog.com/2015/03/backoff.html

    :param value: The unadulterated backoff func.
    :return: random func from range between 0 and func
    """
    return random.uniform(0, value)
