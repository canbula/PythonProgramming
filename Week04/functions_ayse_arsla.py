# custom_power
custom_power = lambda x, /, e=1: x ** e


# custom_equation
def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1
) -> float:
    """
    Calculates the custom equation.

    :param x: First number.
    :param y: Second number.
    :param a: First exponent.
    :param b: Second exponent.
    :param c: Divisor.
    :returns: The result of the equation.
    :rtype: float
    """
    return (x ** a + y ** b) / c


# fn_w_counter
import inspect

def fn_w_counter() -> tuple:
    caller = inspect.currentframe().f_back.f_code.co_name

    fn_w_counter.counter += 1

    if caller in fn_w_counter.callers:
        fn_w_counter.callers[caller] += 1
    else:
        fn_w_counter.callers[caller] = 1

    return fn_w_counter.counter, fn_w_counter.callers.copy()


fn_w_counter.counter = 0
fn_w_counter.callers = {}


# Examples
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
