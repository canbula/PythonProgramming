import os

custom_power = lambda x=0, /, e=1 : x**e

def custom_equation(x: int=0 ,y: int=0,/,a: int=1,b: int=1,*,c: int=1) ->float:
    """
    This function returns a mathematical equation

    :param x:first number to be exponentiated
    :param y:second number to be exponentiated
    :param a:power of the first number
    :param b:power of the second number
    :param c:divisor of the sum of exponentiated
    :return:the result of the equation

    """
    return (x**a + y**b) / c


caller_dict = {}
call_counter = 0

def fn_w_counter() -> (int, dict[str, int]):
    caller = __name__
    global call_counter
    call_counter += 1
    caller_dict[caller] = caller_dict.get(caller, 0) + 1
    return call_counter, caller_dict