def custom_power(x : int|float = 0,/,e : int|float = 0) -> int|float:
   return x ** e

def custom_equation(x : int|float = 0,y : int|float = 0,/,a : int|float = 1,b : int|float = 1,*,c : int|float = 1) -> int|float:
    '''
    Calculates the value of the equation: (a*x + b*y) / c
    
    :param x: The first variable in the equation.
    :param y: The second variable in the equation.
    :param a: The exponent for x.
    :param b: The exponent for y.
    :param c: The divisor for the entire expression.
    :return: The result of the equation.
    '''
    return (x**a + y**b) / c
    
def fn_w_counter() -> tuple[int, dict]:
      
      if not hasattr(fn_w_counter, "counter"):
            fn_w_counter.counter = 0
            fn_w_counter.dict_counter = {}

      def counter():
           fn_w_counter.counter += 1
           fn_w_counter.dict_counter[__name__] = fn_w_counter.dict_counter.get(__name__, 0) + 1

      counter()
      return (fn_w_counter.counter, fn_w_counter.dict_counter)  
