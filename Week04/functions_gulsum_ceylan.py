
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
    Calculate a mathematical equation.

    :param x: First integer.
    :param y: Second integer.
    :param a: Exponent for x.
    :param b: Exponent for y.
    :param c: Divisor.
    :return: Calculated result.
    """
    return (x ** a + y ** b) / c


total_calls = 0
calls_by_module = {}


def fn_w_counter() -> (int, dict[str, int]):
    global total_calls

    total_calls += 1
    module_name = __name__

    calls_by_module[module_name] = (
        calls_by_module.get(module_name, 0) + 1
    )

    return total_calls, calls_by_module.copy()
