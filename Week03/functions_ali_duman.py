custom_power = lambda x=0, /, e=1: x**e


def custom_equation(x: int=0, y: int=0, /, a: int=1, b: int=1,*, c: int=1) -> float:
    """
    Calculate a custom equation based on the provided parameters.

    Parameters:
        x (int, optional): The base value for the first term. Defaults to 0.
        y (int, optional): The base value for the second term. Defaults to 0.
        a (int, optional): The exponent for the first term. Defaults to 1.
        b (int, optional): The exponent for the second term. Defaults to 1.
        c (int, optional): The divisor for the final calculation. Defaults to 1.

    Returns:
        float: The result of the custom equation (x**a + y**b) / c.
    """
    return (x**a + y**b) / c


def fn_w_counter() -> tuple[int, dict[str, int]]:
    # Get the caller's name
    caller = globals()['__name__']

    # Initialize function attributes
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.calls_per_caller = {}
    
    # Increment the total call count
    fn_w_counter.total_calls += 1
    
    # Update the call count for this caller
    if caller in fn_w_counter.calls_per_caller:
        fn_w_counter.calls_per_caller[caller] += 1
    else:
        fn_w_counter.calls_per_caller[caller] = 1
    
    # Return the total number of calls and the dictionary of calls per caller
    return fn_w_counter.total_calls, fn_w_counter.calls_per_caller