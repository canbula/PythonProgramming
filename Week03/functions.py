def function_name():
    pass


def fn(arg1, arg2):
    return arg1 + arg2


def fn(arg1=0, arg2=0):
    return arg1 + arg2


def fn(arg1: int = 0, arg2: int = 0) -> int:
    return arg1 + arg2


def fn(arg1: int | float, arg2: int | float) -> tuple[float, float]:
    return arg1 + arg2, arg1 * arg2


fn = lambda arg1, arg2: arg1 + arg2


def fn(arg1=0, arg2=0):
    """This function sums two numbers."""
    return arg1 + arg2


def fn(arg1: int = 0, arg2: int = 0) -> int:
    """
    This function sums two numbers.

    :param arg1: The first number, default is 0
    :type arg1: int
    :param arg2: The second number, default is 0
    :type arg2: int
    :raises TypeError: Both arguments must be integers.
    :return: The sum of the two numbers
    :rtype: int
    """
    if type(arg1) != int or type(arg2) != int:
        raise TypeError("Both arguments must be integers.")
    return arg1 + arg2


def fn(arg1: int = 0, arg2: int = 0) -> int:
    """
    This function sums two numbers.

    Args:
        arg1 (int): The first number, default is 0
        arg2 (int): The second number, default is 0

    Returns:
        int: The sum of the two numbers

    Raises:
        TypeError: Both arguments must be integers.
    """
    return arg1 + arg2


def fn(arg1=0, arg2=0):
    return arg1 + arg2


fn(), fn(3), fn(3, 5), fn(arg1=3) 
fn(arg2=5), fn(arg1=3, arg2=5)


def fn(arg1=0, arg2=0, *, arg3=1):
    return (arg1 + arg2) * arg3


fn(), fn(3), fn(3, 5), fn(arg1=3), fn(arg2=5)
fn(arg1=3, arg2=5), fn(3, 5, arg3=2)
fn(arg1=3, arg2=5, arg3=2)
fn(arg3=2, arg1=3, arg2=5)


fn(3, 5, 2)
fn(arg3=2, 3, 5)


def fn(arg1=0, arg2=0, /, arg3=1, arg4=1, *, arg5=1, arg6=1):
    return (arg1 + arg2) * arg3 / arg4 * arg5**arg6


fn(), fn(3), fn(3, 5), fn(3, 5, 2), fn(3, 5, 2, 4)
fn(3, 5, arg3=2, arg4=4)
fn(3, 5, arg3=2, arg4=4, arg5=7, arg6=8)
fn(3, 5, 2, 4, arg5=7, arg6=8)


fn(3, 5, 2, 4, 7, 8)
fn(arg1=3, arg2=5, arg3=2, arg4=4)
fn(arg1=3, arg2=5, arg3=2, arg4=4, arg5=7, arg6=8)


def fn(*args, **kwargs):
    print(args)  # a tuple of positional arguments
    print(kwargs)  # a dictionary of keyword arguments


def parent_function():
    def nested_function():
        print("I'm a nested function.")
    print("I'm a parent function.")

parent_function()
parent_function.nested_function()


def point(x, y):
    def set_x(new_x):
        nonlocal x
        x = new_x
    def set_y(new_y):
        nonlocal y
        y = new_y
    def get():
        return x, y
    point.set_x = set_x
    point.set_y = set_y
    point.get = get
    return point
