import inspect

# A short function to calculate x to the power of e.
custom_power = lambda x=0, /, e=1: x ** e

# Calculate the equation using the given numbers.
def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1,
) -> float:
    """Calculate the sum of two powers divided by a coefficient.

    :param x: First base.
    :type x: int
    :param y: Second base.
    :type y: int
    :param a: Exponent of the first base.
    :type a: int
    :param b: Exponent of the second base.
    :type b: int
    :param c: Divisor (must not be zero).
    :type c: int
    :returns: The result of (x**a + y**b) / c.
    :rtype: float
    :raises ZeroDivisionError: If c is zero.
    """
    # Divide the sum of the powers by c.
    return (x ** a + y ** b) / c

def fn_w_counter() -> tuple[int, dict[str, int]]:
    """Return total number of calls and counts by caller name."""
    # Find the function that called this one.
    caller_name = inspect.currentframe().f_back.f_code.co_name
    # Update the total count and the count for this caller.
    fn_w_counter.count += 1
    fn_w_counter.callers[caller_name] = fn_w_counter.callers.get(caller_name, 0) + 1
    # Return a copy so the saved counts do not change outside.
    return fn_w_counter.count, fn_w_counter.callers.copy()

# Starting values for the counters.
fn_w_counter.count = 0
fn_w_counter.callers = {}
