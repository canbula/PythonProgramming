def fn_w_counter() -> tuple[int, dict[str, int]]:
    """
    Counts function calls with caller information.

    :return: A tuple containing total call count and a dictionary
             mapping caller names to their call counts.
    """
    if not hasattr(fn_w_counter, "_total_calls"):
        fn_w_counter._total_calls = 0
        fn_w_counter._callers = {}

    caller = __name__

    fn_w_counter._total_calls += 1
    fn_w_counter._callers[caller] = fn_w_counter._callers.get(caller, 0) + 1

    return fn_w_counter._total_calls, fn_w_counter._callers
