custom_power = lambda x=0, /, e=1: x**e
"""lambda x=0 / e=1 → x**e"""


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """(x**a + y**b) / c"""
    return (x**a + y**b) / c


def fn_w_counter() -> tuple[int, dict[str, int]]:
    caller = __name__ if __name__ != "<lambda>" else "lambda"
    fn_w_counter.total = getattr(fn_w_counter, "total", 0) + 1
    fn_w_counter.callers = getattr(fn_w_counter, "callers", {})
    fn_w_counter.callers[caller] = fn_w_counter.callers.get(caller, 0) + 1
    return fn_w_counter.total, fn_w_counter.callers.copy()
