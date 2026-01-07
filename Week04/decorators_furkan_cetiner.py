from __future__ import annotations

import time
import tracemalloc
from functools import wraps
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def performance(func: F) -> F:

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # ensure stats exist
        wrapper.counter += 1  # type: ignore[attr-defined]

        # time
        t0 = time.perf_counter()

        # memory (tracemalloc)
        tracing_already = tracemalloc.is_tracing()
        if not tracing_already:
            tracemalloc.start()

        before_current, before_peak = tracemalloc.get_traced_memory()
        try:
            result = func(*args, **kwargs)
        finally:
            after_current, after_peak = tracemalloc.get_traced_memory()
            dt = time.perf_counter() - t0

            wrapper.total_time += dt  # type: ignore[attr-defined]

            # Use peak delta as "consumed" approximation for this call
            delta_peak = after_peak - before_peak
            if delta_peak < 0:
                delta_peak = 0
            wrapper.total_mem += int(delta_peak)  # type: ignore[attr-defined]

            # Don't disrupt global tracing if it was already enabled
            if not tracing_already:
                tracemalloc.stop()

        return result

    # required attributes
    wrapper.counter = 0       # type: ignore[attr-defined]
    wrapper.total_time = 0.0  # type: ignore[attr-defined]
    wrapper.total_mem = 0     # type: ignore[attr-defined]

    return cast(F, wrapper)