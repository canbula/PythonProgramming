custom_power = lambda x = 0, /,  e = 1 : x ** e

def custom_equation(x = 0, y = 0, /, a = 1, b = 1, *, c = 1):
    """
    This function calculates (x ** a + y ** b) / c.
    
    :param x: First number (positional only, default 0)
    :param y: Second number (positional only, default 0)
    :param a: Third number (positional or keyword, default 1)
    :param b: Fourth number (positional or keyword, default 1)
    :param c: Fifth number (keyword only, default 1)
    :return: (x ** a + y ** b) / c
    """

    return (x ** a + y ** b) / c



