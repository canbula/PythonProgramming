from typing import Literal


def check_methods(subcls, *methods) -> Literal["NotImplemented"] | Literal[True]:
    """
    Check if a subclass implements the specified methods.

    :param subcls: The potential subclass.
    :param methods: The methods to be checked.
    :return: NotImplemented if any method is not implemented, True otherwise.
    :rtype: Literal["NotImplemented"] | Literal[True]
    """
    mro: dict = subcls.__mro__
    for method in methods:
        for cls in mro:
            if method in cls.__dict__:
                if cls.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True
