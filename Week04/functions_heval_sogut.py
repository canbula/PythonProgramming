# custom_power
custom_power = lambda x=0, /, e=1: x**e

# custom_equation
def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result of the equation (x**a + y**b) / c.

    :param x: The first base number (positional-only).
    :param y: The second base number (positional-only).
    :param a: The exponent for x (positional-or-keyword).
    :param b: The exponent for y (positional-or-keyword).
    :param c: The divisor (keyword-only).
    :return: The float result of the equation.
    """
    # Manual type checking to raise TypeError
    if not isinstance(x, int):
        raise TypeError("x must be an integer")
    if not isinstance(y, int):
        raise TypeError("y must be an integer")
    if not isinstance(a, int):
        raise TypeError("a must be an integer")
    if not isinstance(b, int):
        raise TypeError("b must be an integer")
    if not isinstance(c, int):
        raise TypeError("c must be an integer")
    
    # The calculation, which will return a float
    return (x**a + y**b) / c

# fn_w_counter
def fn_w_counter() -> (int, dict[str, int]):
    """
    Counts the total number of times this function has been called.

    This function uses an attribute 'count' on itself to store the call count,
    avoiding the use of a global variable.

    Returns the total count and a dictionary where the key is this
    module's __name__ and the value is the total count.

    :return: A tuple of (total_calls, {__name__: total_calls})
    :rtype: (int, dict[str, int])
    """
    # Initialize the counter on the function object if it doesn't exist
    if not hasattr(fn_w_counter, "count"):
        fn_w_counter.count = 0
    
    # Increment the counter
    fn_w_counter.count += 1
    
    # Return the total count and the dictionary as specified
    return (fn_w_counter.count, {__name__: fn_w_counter.count})
