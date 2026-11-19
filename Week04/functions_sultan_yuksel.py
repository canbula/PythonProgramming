custom_power = lambda x = 0, / , e = 1: x**e


def custom_equation (x: int = 0, y: int = 0, / , a: int = 1, b: int = 1, * , c: int = 1) -> float:
  '''
  This function calculates the custom equation (x**a + y**b)/c

  :param x: Positional-only x value, defaults to 0
  :type x: int, optional
  :param y: Positional-onlyr y value, defaults to 0
  :type y: int, optional
  :param a: Positional-or-keyword exponent for x, defaults to 1
  :type a: int, optional
  :param b: Positional-or-keyword exponent for y, defaults to 1
  :type b: int, optional
  :param c: Keyword-only division of the sum, defaults to 1
  :type c: int, optional
  :return: Result of (x**a + y**b)/c
  :rtype: float

  '''
  return (x**a + y**b)/c


def fn_w_counter() -> tuple[int, dict[str, int]]:
  if not hasattr(fn_w_counter, "counter"):
    fn_w_counter.counter = 0
    fn_w_counter.callers = {}
  fn_w_counter.counter += 1
  if __name__ in fn_w_counter.callers:
    fn_w_counter.callers[__name__] += 1
  else:
    fn_w_counter.callers = 1
  return fn_w_counter.counter, fn_w_counter.callers
  
