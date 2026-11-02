custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /,
                    a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """Calculate a sum of powers divided by c.

    :param x: First base.
    :param y: Second base.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Divisor.
    :return: The value of (x**a + y**b) / c.
    :raises TypeError: If an argument is not an integer.
    """
    if not all(isinstance(value, int) for value in (x, y, a, b, c)):
        raise TypeError("All arguments must be integers")
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    """Count calls and keep a per-module record."""
    fn_w_counter.counter += 1
    calls = fn_w_counter.calls
    calls[__name__] = calls.get(__name__, 0) + 1
    return fn_w_counter.counter, dict(calls)


fn_w_counter.counter = 0
fn_w_counter.calls = {}
