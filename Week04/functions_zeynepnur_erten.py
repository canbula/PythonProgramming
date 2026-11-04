custom_power = lambda x=0, /, e=1: x**e

def custom_equation (x: int = 0, y: int=0, /, a: int =1, b: int=1, *, c: int=1) -> float:
    """
    This function is used to calculate a custom equation
    :param x: first base
    :param y: second base
    :param a: exponent for x
    :param b: exponent for y
    :param c: divisor
    :return: the result of equation (x**a + y**b)/c
    """
    return float((x**a + y**b)/c)

counter = {}
def fn_w_counter() -> (int, dict[str, int]):
    caller = __name__
    counter[caller] = counter.get(caller,0) + 1
    return sum(counter.values()), counter

