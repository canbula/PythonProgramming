# custom_power (lambda)
custom_power = lambda x=0, e=1: x ** e


def custom_equation(
    x: int = 0,
    y: int = 0,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1
) -> float:
    """
    :param x: integer value
    :param y: integer value
    :param a: integer value
    :param b: integer value
    :param c: integer value
    :return: result of equation
    """
    if not all(isinstance(v, int) for v in (x, y, a, b, c)):
        raise TypeError("All parameters must be int")

    return (x ** a + y ** b) / c


_call_count = 0

def fn_w_counter() -> (int, dict[str, int]):
    global _call_count
    _call_count += 1
    return _call_count, {__name__: _call_count}
