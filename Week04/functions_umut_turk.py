custom_power = lambda x= 0, /, e = 1: x ** e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """Calculate custom polynomial equation result.

    Calculates :math:`\\frac{x^a + y^b}{c}`.

    :param x: Positional-only x value, defaults to 0
    :type x: int, optional
    :param y: Positional-only y value, defaults to 0
    :type y: int, optional
    :param a: Positional-or-keyword exponent for x, defaults to 1
    :type a: int, optional
    :param b: Positional-or-keyword exponent for y, defaults to 1
    :type b: int, optional
    :param c: Keyword-only denominator, defaults to 1
    :type c: int, optional
    :return: Result of (x**a + y**b) / c
    :rtype: float
    """
    return (x**a + y**b) / c

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "counter"):
        fn_w_counter.counter = 0
    fn_w_counter.counter += 1
    return (fn_w_counter.counter, {fn_w_counter.__module__: fn_w_counter.counter})
if __name__ == "__main__":
    print(fn_w_counter())