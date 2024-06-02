import sqlite3
from typing import Self
from functools import cache, reduce
from sql_formatter.core import format_sql
from sys import getsizeof
import math
from psutil import virtual_memory
import customtkinter
from .event_handler import EventHandler
from ..utils import QUERY_ERROR_NONE_OBJECT


class SQLEventHandler(EventHandler):
    """Handler for SQL events."""

    MAX_PAGE_COUNT: int = 10
    queries: list[str] = []
    query_index: int = 0

    @cache
    def __new__(cls, *args, **kwargs) -> Self:
        """
        Create a new instance of SQLEventHandler class.
        Implements the Singleton pattern.
        """
        return super().__new__(cls)

    def __init__(
        self, query: str, cursor: sqlite3.Cursor, result_label: customtkinter.CTkLabel
    ) -> None:
        """
        Initialize the SQLEventHandler instance.
        If the singleton query has not been created, it initializes the attributes accordingly.

         :param query: The SQL query.
         :type query: str
         :param cursor: The cursor for executing the query.
         :type cursor: sqlite3.Cursor
         :param result_label: The label to display the result.
         :type result_label: customtkinter.CTkLabel
        """
        if not hasattr(self, "_query"):
            self._query: str = query
            self._cursor: sqlite3.Cursor = cursor
            self._result_label: customtkinter.CTkLabel = result_label
            self.__col_len: int = 0
            self.__row_len: int = 0
            self.__total_size: int = 0
            self.queries.append(format_sql(query, max_len=1000000000))
            self.query_index += 1

    @property
    def get_query(self) -> str:
        """
        Get the SQL query.

        :return: The SQL query. otherwise None.
        :rtype: str| None
        """
        if not sqlite3.complete_statement(self._query):
            return QUERY_ERROR_NONE_OBJECT
        return self._query

    @property
    def get_query_result_itr(self) -> sqlite3.Cursor | None:
        """

        Get the iterator for executing the SQL query.

        :return: Iterator for executing the SQL query. Returns None if there is an error.
        :rtype: sqlite3.Cursor or None
        :raise KeyError: Raised in a specific error condition.
        """
        try:
            return self._cursor.execute(self.get_query)
        except (sqlite3.ProgrammingError, AttributeError) as error:
            print(error)
            return QUERY_ERROR_NONE_OBJECT

    @staticmethod
    def _sizeof_row(row: list[tuple]) -> int:
        """
        Calculate the size of a row in bytes.

        :param row: List of tuples representing a row.
        :type row: list[tuple]
        :return: Size of the row in bytes.
        :rtype: int
        """
        return reduce(getsizeof, [str(atr) for atr in row])

    @property
    def row_len(self) -> int:
        """
        Get the length of the rows.

        If the row length attribute is not set, it returns the length calculated from the result set.

        :return: Length of the rows.
        :rtype: int
        """
        return self.__row_len or len(self)

    @cache
    def __len__(self) -> int:
        """
        Get the total number of rows in the result set.

        This method iterates through the result set obtained from the query execution and counts the rows. It also
        calculates the total size of the result set.

        :return: Total number of rows in the result set.
        :rtype: int
        :raise KeyError: Raised in a specific error condition.
        """
        try:
            row_itr: sqlite3.Cursor = self.get_query_result_itr
            row: list[tuple] = next(row_itr)
            self.__col_len = len(row)
            self.__total_size += self._sizeof_row(row)
            for row_count, row in enumerate(row_itr):
                self.__total_size += self._sizeof_row(row)
            self.__row_len = row_count + 1
            return self.__row_len
        except (sqlite3.ProgrammingError, StopIteration, TypeError) as error:
            return 0

    @property
    @cache
    def col_len(self) -> int:
        """
        Get the total number of columns in the result set.

        This method returns the number of columns in the result set.

        :return: Total number of columns in the result set.
        :rtype: int

        """
        return self.__col_len

    @property
    def divaded_itrs(self) -> tuple[sqlite3.Cursor]:
        """
        Divide the result set into multiple cursors.

        This method divides the result set into multiple cursors based on the available memory and the size of the result set.
        It calculates the number of pages and rows per page, then creates cursors accordingly.

        :return: Tuple of cursors representing the divided result set.
        :rtype: tuple[sqlite3.Cursor]
        :raise KeyError: Raised in a specific error condition.
        """
        len(self)
        avaible_memory: int = int(virtual_memory()[1])

        page_count: int = max(
            min(
                math.ceil(self.__total_size // (avaible_memory / 4.0)),
                self.MAX_PAGE_COUNT,
            ),
            1,
        )
        row_count: int = self.__total_size // page_count

        try:
            itrs: sqlite3.Cursor = [
                self.get_query_result_itr for _ in range(page_count)
            ]
        except TypeError:
            return QUERY_ERROR_NONE_OBJECT

        try:
            for current_page, itr in enumerate(itrs[1:], 1):
                for _ in range(current_page * row_count):
                    next(itr)
        except IndexError:
            return itrs

        return itrs

    def handle(self) -> tuple[sqlite3.Cursor]:
        """
        Handle the SQL query result.

        This method retrieves the divided iterators of the SQL query result using the `divaded_itrs` method and returns them.

        :return: Tuple of cursors representing the divided result set.
        :rtype: tuple

        """
        return self.divaded_itrs
