# ---------- custom_power ----------

custom_power = lambda x, e=1: x ** e


# ---------- custom_equation ----------

def custom_equation(x, y=0, *, a=0, b=1, c=1) -> float:
    """
    Computes the equation: (x**a + y**b) / c
    """
    return (x ** a + y ** b) / c


# ---------- fn_w_counter ----------

def fn_w_counter():
    total_calls = 0
    callers = {}

    def inner():
        nonlocal total_calls
        total_calls += 1

        caller_name = __name__
        callers[caller_name] = callers.get(caller_name, 0) + 1

        return total_calls, callers

    return inner

