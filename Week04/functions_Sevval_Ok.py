custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1
) -> float:
    return (x ** a + y ** b) / c

_call_total = 0
_callers = {}

def fn_w_counter():
    global _call_total, _callers

    caller = __name__
    _call_total += 1
    _callers[caller] = _callers.get(caller, 0) + 1

    return _call_total, _callers
