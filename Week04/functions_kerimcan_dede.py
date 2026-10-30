custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(x: int=0, y: int=0, /, a: int=1, b: int=1, *, c: int=1) -> float:
    """
    This function does arithmetic opearations.

    :param1: first number to be exponantiated
    :param2: second number to be exponantiated
    :param3: power of the first number
    :param4: power of the second number
    :param5: divisor of sum of exponantiated numbers

    :result: division the sum of exponantiated numbers
    """
    return (x**a + y**b) / c

call_counter = 0
caller_dict = {}
def fn_w_counter() -> (int, dict):
    caller = __name__
    global call_counter
    call_counter += 1
    if caller in caller_dict:
        caller_dict[caller] += 1
    else:
        caller_dict[caller] = 1
    return call_counter, caller_dict
