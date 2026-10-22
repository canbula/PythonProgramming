import sys

custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Raises x to the power a and y to the power b, adds them and divides by c.

    :param x: Base of the first term (positional-only)
    :type x: int
    :param y: Base of the second term (positional-only)
    :type y: int
    :param a: Power applied to x
    :type a: int
    :param b: Power applied to y
    :type b: int
    :param c: Number to divide the sum by (keyword-only)
    :type c: int
    :return: The calculated value
    :rtype: float
    """
    first_term = x ** a
    second_term = y ** b
    return float((first_term + second_term) / c)


def _make_counter():
    calls = {"count": 0}
    by_caller = {}

    def fn_w_counter() -> tuple[int, dict[str, int]]:
        name = sys._getframe(1).f_globals.get("__name__")
        calls["count"] += 1
        if name in by_caller:
            by_caller[name] += 1
        else:
            by_caller[name] = 1
        return calls["count"], by_caller

    return fn_w_counter


fn_w_counter = _make_counter()
