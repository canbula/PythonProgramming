def custom_power(x=0, /, e=1):
    return pow(x, e)


def custom_equation(x: int = 0, y: int = 0, /,
                   a: int = 1, b: int = 1, *,
                   c: int = 1) -> float:

    first_result = pow(x, a)
    second_result = pow(y, b)

    return (first_result + second_result) / c


total_calls = 0
caller_counts = {}


def fn_w_counter() -> tuple[int, dict[str, int]]:

    global total_calls, caller_counts

    total_calls += 1

    caller = __name__
    caller_counts[caller] = caller_counts.get(caller, 0) + 1

    return total_calls, caller_counts.copy()
