custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(
    x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """Calculate (x ** a + y ** b) / c.

    :param x: First base.
    :param y: Second base.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Divisor.
    :return: The result as a float.
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")

    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "total_count"):
        fn_w_counter.total_count = 0
        fn_w_counter.call_records = {}

    caller = __name__
    fn_w_counter.total_count += 1

    if caller not in fn_w_counter.call_records:
        fn_w_counter.call_records[caller] = 1
    else:
        fn_w_counter.call_records[caller] += 1

    return fn_w_counter.total_count, fn_w_counter.call_records
