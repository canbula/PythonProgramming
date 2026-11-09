custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Computes (x**a + y**b) / c.

    :param x: First base
    :param y: Second base
    :param a: Exponent of x
    :param b: Exponent of y
    :param c: Divisor
    :return: (x**a + y**b) / c
    """
    if not all(isinstance(i, int) for i in (x, y, a, b, c)):
        raise TypeError("All parameters must be integers")
    return (x ** a + y ** b) / c


counter = {}


def fn_w_counter() -> (int, dict[str, int]):
    counter[__name__] = counter.get(__name__, 0) + 1
    return sum(counter.values()), counter
