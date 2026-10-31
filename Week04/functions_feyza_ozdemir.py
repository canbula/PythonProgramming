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
    This function calculates the result of a custom mathematical equation.

    :param x: The first base value (positional-only), defaults to 0.
    :type x: int
    :param y: The second base value (positional-only), defaults to 0.
    :type y: int
    :param a: The first exponent (positional-or-keyword), defaults to 1.
    :type a: int
    :param b: The second exponent (positional-or-keyword), defaults to 1.
    :type b: int
    :param c: The divisor (keyword-only), defaults to 1.
    :type c: int
    :return: The result of (x**a + y**b) / c as a float.
    :rtype: float
    """
    return float((x ** a + y ** b) / c)


def fn_w_counter() -> tuple[int, dict[str, int]]:
    """
    This function counts total function calls and tracks calls per caller module.

    :return: A tuple containing the total call count and a dictionary of caller counts.
    :rtype: tuple[int, dict[str, int]]
    """
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_globals.get("__name__", "__main__") if caller_frame else "__main__"

    fn_w_counter.total_calls += 1
    fn_w_counter.caller_counts[caller_name] = fn_w_counter.caller_counts.get(caller_name, 0) + 1

    return fn_w_counter.total_calls, dict(fn_w_counter.caller_counts)


fn_w_counter.total_calls = 0
fn_w_counter.caller_counts = {}