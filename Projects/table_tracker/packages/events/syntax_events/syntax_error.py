from ..event_handler import EventHandler
import customtkinter
import sqlite3


class SytanxErrorHandler(EventHandler):
    """
    Class for syntax error handling.

    SytanxErrorHandler class is used for detecting and highlighting syntax errors in a text box.
    """

    PASS_UNNECASSARY_LAST_LETTERS: int = 2
    ON_OFF: dict[str, bool] = {"On": True, "Off": False}

    def __init__(self, root: "App") -> None:
        """
        Initializes a SytanxErrorHandler instance.

        :param root: The root of the application.
        :type root: App
        """
        self._root: "App" = root
        self._last_syntax_error_index = customtkinter.END
        self.__syntax_error_highlight: bool = True

    def add_syntax_error_sign(self) -> None:
        """
        Adds a syntax error sign to the text box.

        :return: None.
        """
        self._last_syntax_error_index = (
            len(self._root.get_textbox_text.strip("\n"))
            - self.PASS_UNNECASSARY_LAST_LETTERS
            if self._last_syntax_error_index == customtkinter.END
            or self._last_syntax_error_index
            >= len(self._root.get_textbox_text.strip("\n"))
            else self._last_syntax_error_index
        )
        parsed_tk_len: str = f"1.0+{self._last_syntax_error_index}c"
        self._root.textbox.tag_add(
            self.__SYNTAX_ERROR_TAG_NAME, parsed_tk_len, customtkinter.END
        )
        self._root.textbox.tag_config(
            self.__SYNTAX_ERROR_TAG_NAME, underline=True, underlinefg="red"
        )

    def change_syntax_on_off(self, curren_state: str) -> None:
        """
        Changes the syntax error highlighting state.

        :param curren_state: The current state ("On" or "Off").
        :type curren_state: str
        :return: None.
        """
        self.__syntax_error_highlight = self.ON_OFF[curren_state]

    def handle(self) -> None:
        """
        Handles syntax errors.

        :return: None.
        """
        if self.__syntax_error_highlight:
            if not sqlite3.complete_statement(self._root.get_textbox_text):
                self.add_syntax_error_sign()
            else:
                self._root.textbox.tag_delete(self.__SYNTAX_ERROR_TAG_NAME)
                self._last_syntax_error_index = customtkinter.END

    @property
    def __SYNTAX_ERROR_TAG_NAME(self) -> str:
        """
        Returns the syntax error tag name.

        :return: The syntax error tag name.
        :rtype: str
        """
        return "syntax_error_tag_name"
