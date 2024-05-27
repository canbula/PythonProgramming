custom_power = lambda x = 0 , / ,e = 1, : x**e 


def custom_equation(x: int=0, y: int=0, /, a: int=1, b: int=1,*, c: int=1) -> float:
    """
    This function raises x to the power of a, 
    adds y to the power of b, 
    then divides this sum by c, 
    and returns the result as a floating-point number.
    
    :param x : First Number 
    :param y : Second Number 
    :param a : Third Number 
    :param b : Fourth Number 
    :param c : Fifth Number 
    :return: result as a floating-point number.
    """
    return float((x**a + y **b ) / c)


def fn_w_counter() -> (int, dict[str, int]):
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