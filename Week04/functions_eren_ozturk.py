custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """Computes (x**a + y**b) / c.

    :param x: First base
    :param y: Second base
    :param a: Exponent of x
    :param b: Exponent of y
    :param c: Divisor
    :return: (x**a + y**b) / c
    """
    return (x ** a + y ** b) / c


calls = {}


def fn_w_counter() -> tuple[int, dict[str, int]]:
    calls[__name__] = calls.get(__name__, 0) + 1
    return sum(calls.values()), calls