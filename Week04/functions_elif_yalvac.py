custom_power = lambda x=0, /, e=1: x ** e



def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates a specific mathematical expression.

    :param x: Positional-only, default 0
    :param y: Positional-only, default 0
    :param a: Positional or keyword, default 1
    :param b: Positional or keyword, default 1
    :param c: Keyword-only, default 1
    :return: Returns (x**a + y**b) / c as a float
    """
    return (x ** a + y ** b) / c




from collections import defaultdict
import inspect
_total_calls = 0
_caller_counts = defaultdict(int)
def fn_w_counter() -> tuple[int, dict[str, int]]:
    global _total_calls
    _total_calls += 1
    caller = inspect.currentframe().f_back.f_globals.get('__name__', '<unknown>')
    _caller_counts[caller] += 1
    return _total_calls, dict(_caller_counts)
