# custom_power: A lambda function
# - Two parameters (x and e)
# - x is positional-only
# - e is positional-or-keyword
# - x has default value 0
# - e has default value 1
# - Returns x**e
custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    A custom equation that calculates (x**a + y**b) / c
    
    :param x: First integer value (positional-only, default 0)
    :param y: Second integer value (positional-only, default 0)
    :param a: Exponent for x (positional-or-keyword, default 1)
    :param b: Exponent for y (positional-or-keyword, default 1)
    :param c: Divisor (keyword-only, default 1)
    :return: The result of (x**a + y**b) / c as a float
    """
    # Type checking
    if not isinstance(x, int) or isinstance(x, bool):
        raise TypeError("x must be an integer")
    if not isinstance(y, int) or isinstance(y, bool):
        raise TypeError("y must be an integer")
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError("a must be an integer")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError("b must be an integer")
    if not isinstance(c, int) or isinstance(c, bool):
        raise TypeError("c must be an integer")
    
    return (x ** a + y ** b) / c


# fn_w_counter: A function that counts calls
# - Returns a tuple of (call_count, {module_name: call_count})
# - Uses a closure to maintain state
_counter = 0
_module_name = __name__

def fn_w_counter() -> (int, dict[str, int]):
    """
    A function that counts the number of times it has been called.
    
    :return: A tuple containing the call count and a dictionary with module info
    """
    global _counter
    _counter += 1
    return (_counter, {_module_name: _counter})
