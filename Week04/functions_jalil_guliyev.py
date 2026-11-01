"""Week 04: Functions homework."""

custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(
    x: int = 0, y: int = 0, /,
    a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """Calculate a polynomial-style expression.

    :param x: First integer base.
    :param y: Second integer base.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Integer divisor, which must not be zero.
    :return: The value of (x ** a + y ** b) / c as a float.
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    """Return the total calls and per-module call counts."""
    fn_w_counter.total += 1
    caller = __name__
    fn_w_counter.callers[caller] = fn_w_counter.callers.get(caller, 0) + 1
    return fn_w_counter.total, fn_w_counter.callers.copy()


fn_w_counter.total = 0
fn_w_counter.callers = {}
