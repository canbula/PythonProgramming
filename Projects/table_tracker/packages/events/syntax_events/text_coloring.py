from typing import Any

from ..event_handler import EventHandler
from packages.utils import SQLKeyWords
import customtkinter
import string


class TextColoringHandler(EventHandler, metaclass=SQLKeyWords):
    """
    Class for text coloring handling.

    TextColoringHandler class is used for coloring specific words in a text box.
    """

    def __init__(self, root: "App") -> None:
        """
        Initializes a TextColoringHandler instance.

        :param root: The root of the application.
        :type root: App
        """
        self._root: "App" = root

    def handle(self) -> None:
        """
        Performs the text coloring operation.

        :return: None.
        """
        for word in self.keywords_dict:
            self.__coloring_words(word=word)
            self.__coloring_words(word=word.casefold())

    def __coloring_words(self, word: str, start_index: str = "1.0") -> None:
        """
        Colors a specific word in the text box.

        :param word: The word to be colored.
        :type word: str
        :param start_index: The starting index. Default is "1.0".
        :type start_index: str
        :return: None.
        """
        while True:
            start_index = self._root.textbox.search(
                word, start_index, stopindex=customtkinter.END
            )

            if not bool(start_index):
                break

            end_index: str = f"{start_index}+{len(word)}c"

            if self.__is_keyword(start_index=start_index, word=word):
                self._root.textbox.tag_add(word, start_index, end_index)
                self._root.textbox.tag_config(
                    word, foreground=self.keywords_dict[word.upper()]
                )
            start_index = end_index

    def __is_keyword(self, start_index: str = "1.0", word: str = "") -> bool:
        """
        Checks if a word is a SQL keyword.

        :param start_index: The starting index.
        :type start_index: str
        :param word: The word to be checked.
        :type word: str
        :return: True if the word is a SQL keyword, False otherwise.
        :rtype: bool
        """
        post_letters: str = self._root.textbox.get(
            start_index, f"{start_index}+{len(word)+1}c"
        )
        if start_index != "1.0":
            pre_word_index: str = f"{start_index}-{1}c"
            pre_letters: str = self._root.textbox.get(pre_word_index, start_index)
            return (
                bool(set(pre_letters) - set(string.ascii_letters))
                and " " in post_letters
            )
        return " " in post_letters
