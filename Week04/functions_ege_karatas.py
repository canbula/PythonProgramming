custom_power = lambda x, /, e=1: x**e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates a custom mathematical equation: (x**a + y**b) / c.

    :param x: The base for the first term, must be passed positionally.
              Defaults to 0.
    :type x: int
    :param y: The base for the second term, must be passed positionally.
              Defaults to 0.
    :type y: int
    :param a: The exponent for the first term, can be passed positionally or by keyword.
              Defaults to 1.
    :type a: int
    :param b: The exponent for the second term, can be passed positionally or by keyword.
              Defaults to 1.
    :type b: int
    :param c: The divisor, must be passed by keyword.
              Defaults to 1.
    :type c: int
    :returns: The result of the calculation.
    :rtype: float
    """
    return (x**a + y**b) / c


def fn_w_counter(func):
    total_calls = 0
    caller_counts = {}

    def wrapper(*args, **kwargs):
        nonlocal total_calls, caller_counts

        total_calls += 1
        caller = func.__module__
        caller_counts[caller] = caller_counts.get(caller, 0) + 1
        return total_calls, caller_counts

    return wrapper
