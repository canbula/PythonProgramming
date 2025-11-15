# -------------
# custom_power
# -------------
custom_power = lambda x=0, e=1: x**e


# ------------------
# custom_equation
# ------------------
def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    return (x**a + y**b) / c

# -------------
# fn_w_counter
# -------------

from typing import Tuple, Dict

def fn_w_counter(_state={'total': 0, 'callers': {}}) -> Tuple[int, Dict[str,int]]:
    _state['total'] += 1
    caller = __name__
    _state['callers'][caller] = _state['callers'].get(caller, 0) + 1
    return _state['total'], _state['callers']
    
    
#  custom_power test
print(custom_power(2,3))  

# custom_equation test
print(custom_equation(2,3))       
print(custom_equation(3,5,a=2,b=3,c=4)) 

# fn_w_counter test
for i in range(10):
    fn_w_counter()
print(fn_w_counter())  # (11, {'__main__': 11})

