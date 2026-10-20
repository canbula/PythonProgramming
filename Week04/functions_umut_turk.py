custom_power = lambda x= 0, /, e = 1: x ** e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """_summary_

    Args:
        x (int, optional): _description_. Defaults to 0. positional only
        y (int, optional): _description_. Defaults to 0. positional only
        a (int, optional): _description_. Defaults to 1. positional or keyword
        b (int, optional): _description_. Defaults to 1. positional or keyword
        c (int, optional): _description_. Defaults to 1. keyword only

    Returns:
        float: _description_
        x**a + y**b / c
    """
    return (x**a + y**b) / c

def fn_w_counter():
    if not hasattr(fn_w_counter, "counter"):
        fn_w_counter.counter = 0
    fn_w_counter.counter += 1
    return (fn_w_counter.counter, {fn_w_counter.__module__: fn_w_counter.counter})
if __name__ == "__main__":
    print(fn_w_counter())