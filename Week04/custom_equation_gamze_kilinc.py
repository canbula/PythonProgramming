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
    Calculates a custom mathematical equation.

    :param x: First positional-only integer value.
    :param y: Second positional-only integer value.
    :param a: Exponent for x.
    :param b: Exponent for y.
    :param c: Divisor value.
    :return: The result of (x**a + y**b) / c as a float.
    """
    return (x ** a + y ** b) / c
