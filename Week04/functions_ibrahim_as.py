import sys

custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1,
) -> float:
    """Calculate (x**a + y**b) / c.

    :param x: First base.
    :type x: int
    :param y: Second base.
    :type y: int
    :param a: Exponent of x.
    :type a: int
    :param b: Exponent of y.
    :type b: int
    :param c: Divisor.
    :type c: int
    :returns: The result of the equation.
    :rtype: float
    :raises ZeroDivisionError: If c is zero.
    """
    return (x ** a + y ** b) / c


_total_calls = 0
_caller_counts: dict[str, int] = {}


def fn_w_counter() -> tuple[int, dict[str, int]]:
    """Count calls, grouped by the caller's module name."""
    global _total_calls

    caller_name = sys._getframe(1).f_globals.get("__name__", "<unknown>")

    _total_calls += 1
    _caller_counts[caller_name] = _caller_counts.get(caller_name, 0) + 1

    return _total_calls, _caller_counts.copy()


if __name__ == "__main__":
    print(custom_power(2))                   
    print(custom_power(2, 3))                
    print(custom_power(2, e=2))             

    print(custom_equation(2, 3))             
    print(custom_equation(2, 3, 2))          
    print(custom_equation(2, 3, 2, 3))       
    print(custom_equation(3, 5, a=2, b=3, c=4))  
    print(custom_equation(3, 5, 2, b=3, c=4))    
    print(custom_equation(3, 5, 2, 3, c=4))      

    for i in range(10):
        fn_w_counter()

    print(fn_w_counter())  
