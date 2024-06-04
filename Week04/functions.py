def fn(arg1: int = 0, arg2: int = 0, *, arg3: int = 1) -> int:
    """This function sums two numbers."""
    if type(arg1) != int:
        raise TypeError("Wrong type!")
    return int(arg1 + arg2)


try:
    print(fn(3.5, 5))
except TypeError:
    print("arg1 is wrong typed")


print(fn(3, 5, arg3=7))
