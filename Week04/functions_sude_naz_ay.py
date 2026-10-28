import inspect

custom_power = lambda x=0, /, e=1: x**e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculate the custom equation result based on provided parameters.

    :param x: Positional-only base for first term, default 0
    :type x: int
    :param y: Positional-only base for second term, default 0
    :type y: int
    :param a: Exponent for first term, default 1
    :type a: int
    :param b: Exponent for second term, default 1
    :type b: int
    :param c: Keyword-only divisor, default 1
    :type c: int
    :return: Computed float result of (x**a + y**b) / c
    :rtype: float
    """
    return float((x**a + y**b) / c)


def fn_w_counter() -> tuple[int, dict[str, int]]:
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.callers = {}

    fn_w_counter.total_calls += 1

    # Çağrıyı yapan modülün __name__ değerini tespit eder
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_globals.get("__name__", "__main__")

    fn_w_counter.callers[caller_name] = fn_w_counter.callers.get(caller_name, 0) + 1

    return fn_w_counter.total_calls, fn_w_counter.callers
