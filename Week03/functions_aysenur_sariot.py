custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(x=0, y=0, /, a=1, b=1, *, c=1):
    """
    Computes the expression (x**a + y**b) / c.

    :param x: Positional-only base for exponent a.
    :param y: Positional-only base for exponent b.
    :param a: Exponent for x (positional-or-keyword).
    :param b: Exponent for y (positional-or-keyword).
    :param c: Keyword-only divisor.
    :return: The result of (x**a + y**b) / c.
    """
    return (x ** a + y ** b) / c
  
def fn_w_counter(fn):
    counts = {}
    total_calls = 0

    def wrapper(*args, **kwargs):
        nonlocal total_calls
        total_calls += 1
        caller_name = "__name__"

        counts[caller_name] = counts.get(caller_name, 0) + 1

        result = fn(*args, **kwargs)

        return total_calls, counts

    return wrapper
