def custom_equation(x: int, y: int, a: int, b: int, c: int) -> float:
    """Calculates the custom equation.

    :param x: first base
    :type x: int
    :param y: second base
    :type y: int
    :param a: first exponent
    :type a: int
    :param b: second exponent
    :type b: int
    :param c: divisor
    :type c: int
    :return: the result of (x**a + y**b) / c
    :rtype: float
    """
    return float((x**a + y**b) / c)


def fn_w_counter() -> tuple[int, dict[str, int]]:
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
