from abc import ABCMeta
from typing import Literal
from types import NotImplementedType
from packages.utils import check_methods


class EventHandler(metaclass=ABCMeta):
    """
    Abstract base class for event handling.

    EventHandler class defines the interface for event handling. Subclasses must implement the handle method.
    """

    __slots__: tuple = ()

    @classmethod
    def __subclasshook__(cls, subcls) -> NotImplementedType | Literal[True]:
        """
        Check if a subclass implements the required methods.

        :param subcls: The potential subclass.
        :return: NotImplementedType if the method is not implemented, True otherwise.
        :rtype: NotImplementedType | Literal[True]
        """
        return check_methods(subcls, "handle")
