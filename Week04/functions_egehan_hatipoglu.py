import inspect

custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /,
                    a: int = 1, b: int = 1, *, c: int = 1) -> float:



    return (x**a + y**b) / c


counter = 0
callers = {}


def fn_w_counter() -> tuple:
    global counter

    counter += 1

    caller = inspect.currentframe().f_back.f_globals["__name__"]

    if caller in callers:
        callers[caller] += 1
    else:
        callers[caller] = 1

    return counter, callers.copy()
