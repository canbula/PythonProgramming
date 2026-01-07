from __future__ import annotations

import inspect
from typing import Any, Dict, Tuple


custom_power = lambda x=0, /, e=1: x**e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:

    return (x**a + y**b) / c


def fn_w_counter() -> Tuple[int, Dict[str, int]]:


    if not hasattr(fn_w_counter, "_total"):
        fn_w_counter._total = 0  # type: ignore[attr-defined]
    if not hasattr(fn_w_counter, "_by_caller"):
        fn_w_counter._by_caller = {}  # type: ignore[attr-defined]


    frame = inspect.currentframe()
    caller_frame = frame.f_back if frame is not None else None
    caller_name = "<unknown>"
    if caller_frame is not None:
        caller_name = str(caller_frame.f_globals.get("__name__", "<unknown>"))


    fn_w_counter._total += 1  # type: ignore[attr-defined]
    by_caller: Dict[str, int] = fn_w_counter._by_caller  # type: ignore[attr-defined]
    by_caller[caller_name] = by_caller.get(caller_name, 0) + 1


    return int(fn_w_counter._total), dict(by_caller)  # type: ignore[attr-defined]