custom_power = lambda x=0, /, e=1: x ** e
""" / it s means -> value that before / are positionaly """

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = -1, *, c: int = 1) -> float:
    """ value that after * are keyword only
  This function takes x as a power of a, y as a power of b, adds them together, then divides by c and returns the result
  :param x : first parameter
  :param y : second parameter 
  :param a : third parameter 
  :param b : fourth parameter
  :param c : fifth parameter
  :return : ((x**a + y**b) / c)
  """
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "call_counter"):
        fn_w_counter.call_counter = 0
        fn_w_counter.caller_counts = {}

    caller_name = __name__

    fn_w_counter.call_counter += 1

    if caller_name in fn_w_counter.caller_counts:
        fn_w_counter.caller_counts[caller_name] += 1
    else:
        fn_w_counter.caller_counts[caller_name] = 1
    return fn_w_counter.call_counter, fn_w_counter.caller_counts
