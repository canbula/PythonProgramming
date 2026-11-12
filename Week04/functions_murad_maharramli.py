import sys

# 1. Lambda function using the built-in pow() for elegance
custom_power = lambda x=0, /, e=1: pow(x, e)

# 2. Equation function using map() and sum() instead of the standard + operator
def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Evaluates a custom mathematical equation.

    :param x: First base variable (positional-only).
    :param y: Second base variable (positional-only).
    :param a: Exponent for the first variable (positional-or-keyword).
    :param b: Exponent for the second variable (positional-or-keyword).
    :param c: Divisor variable (keyword-only).
    :return: The result of (x**a + y**b) / c as a float.
    """
    # map(pow, (x,y), (a,b)) calculates x**a and y**b simultaneously. 
    return float(sum(map(pow, (x, y), (a, b))) / c)

# 3. Counter function using direct __dict__ manipulation and CPython's sys._getframe
def fn_w_counter() -> tuple[int, dict]:
    # Access the function's internal attribute dictionary directly
    d = fn_w_counter.__dict__
    
    # Increment total calls
    d['total_calls'] = d.get('total_calls', 0) + 1
    
    # Grab the callers dictionary (creates it if it doesn't exist)
    callers = d.setdefault('callers', {})
    
    # sys._getframe(1) is a faster, low-level alternative to the inspect module
    caller = sys._getframe(1).f_globals.get('__name__', 'unknown')
    callers[caller] = callers.get(caller, 0) + 1
    
    return (d['total_calls'], callers)
