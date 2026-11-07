custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    :param x: description
    :param y: description
    :param a: description
    :param b: description
    :param c: description
    :return: description
    """
    for param in (x, y, a, b, c):
        if not isinstance(param, int):
            raise TypeError("must be int")

    return float((x ** a + y ** b) / c)


_counter = 0


def fn_w_counter() -> (int, dict[str, int]):
    global _counter
    _counter += 1
    return _counter, {__name__: _counter}