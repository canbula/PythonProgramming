custom_power = lambda x=0, /, e=1: x**e


def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1,
) -> float:
    """
    Calculate the result of (x**a + y**b) / c.

    :param x: first base (positional-only)
    :type x: int
    :param y: second base (positional-only)
    :type y: int
    :param a: exponent for x (positional-or-keyword)
    :type a: int
    :param b: exponent for y (positional-or-keyword)
    :type b: int
    :param c: divisor (keyword-only)
    :type c: int
    :return: calculated float value
    :rtype: float
    """
    return float((x**a + y**b) / c)


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "call_count"):
        fn_w_counter.call_count = 0
        fn_w_counter.caller_records = {}

    caller_name = __name__
    fn_w_counter.call_count += 1
    fn_w_counter.caller_records[caller_name] = (
        fn_w_counter.caller_records.get(caller_name, 0) + 1
    )
    return fn_w_counter.call_count, fn_w_counter.caller_records