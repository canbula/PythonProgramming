
import inspect

custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1
) -> float:
    """
    Calculate the result of a custom equation.

    :param x: First integer.
    :param y: Second integer.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Divisor.
    :return: Result of the equation.
    """
    return (x ** a + y ** b) / c


def fn_w_counter() -> tuple[int, dict[str, int]]:
    caller = inspect.currentframe().f_back.f_globals["__name__"]

    if not hasattr(fn_w_counter, "counts"):
        fn_w_counter.counts = {}

    counts = fn_w_counter.counts
    counts[caller] = counts.get(caller, 0) + 1

    return sum(counts.values()), counts.copy()
