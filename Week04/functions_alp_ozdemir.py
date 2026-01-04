custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates a specific equation based on inputs.
    
    :param x: The first base (positional only)
    :param y: The second base (positional only)
    :param a: The first exponent
    :param b: The second exponent
    :param c: The divisor (keyword only)
    :return: The calculated float result
    """
    
    if not all(isinstance(arg, int) for arg in [x, y, a, b, c]):
        raise TypeError("All arguments must be integers")
        
    return float((x ** a + y ** b) / c)

_counter = 0

def fn_w_counter() -> (int, dict[str, int]): 
    global _counter
    _counter += 1
    return _counter, {__name__: _counter}
