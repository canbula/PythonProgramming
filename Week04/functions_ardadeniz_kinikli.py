custom_power = lambda x = 0, /, e = 1 : x ** e 

def custom_equation(x: int = 0, y: int= 0, /, a: int=1, b: int=1, *, c: int=1) -> float:
    """
    This function computes the result of the expression (x**a + y**b) / c.

    :param x: The base for the first exponentiation. Positional-only.
    :type x: int
    :param y: The base for the second exponentiation. Positional-only.
    :type y: int
    :param a: The exponent for x. Positional-or-keyword.
    :type a: int
    :param b: The exponent for y. Positional-or-keyword.
    :type b: int
    :param c: The divisor. Keyword-only. Defaults to 1.
    :type c: int
    :returns: The result of the calculation.
    :rtype: float
    
    """
    return (custom_power(x,a) + custom_power(y,b))/c

def fn_w_counter() -> tuple[int, dict[str, int]]:
    if not hasattr(fn_w_counter, "count"):
        setattr(fn_w_counter, "count", 0)
    fn_w_counter.count += 1
    temp_dict = {}
    temp_dict[(str)(__name__)] = fn_w_counter.count
    temp_tuple = (fn_w_counter.count, temp_dict)
    return temp_tuple 

if __name__ == "__main__":
    print(custom_power(2,3))
    print(custom_power(2,e=3))    
    print(custom_equation(2, 2, a=3, b=3,c=1))
    for i in range(5):
        fn_w_counter()
    print(fn_w_counter())