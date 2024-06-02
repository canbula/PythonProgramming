from itertools import cycle
from typing import Any, Self
import string
from abc import ABCMeta


class SQLKeyWords(ABCMeta):
    keywords: set = {
        "ABORT",
        "ACTION",
        "ADD",
        "AFTER",
        "ALL",
        "ALTER",
        "ALWAYS",
        "ANALYZE",
        "AND",
        "AS",
        "ASC",
        "ATTACH",
        "AUTOINCREMENT",
        "BEFORE",
        "BEGIN",
        "BETWEEN",
        "BY",
        "CASCADE",
        "CASE",
        "CAST",
        "CHECK",
        "COLLATE",
        "COLUMN",
        "COMMIT",
        "CONFLICT",
        "CONSTRAINT",
        "CREATE",
        "CROSS",
        "CURRENT",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "DATABASE",
        "DEFAULT",
        "DEFERRABLE",
        "DEFERRED",
        "DELETE",
        "DESC",
        "DETACH",
        "DISTINCT",
        "DO",
        "DROP",
        "EACH",
        "ELSE",
        "END",
        "ESCAPE",
        "EXCEPT",
        "EXCLUDE",
        "EXCLUSIVE",
        "EXISTS",
        "EXPLAIN",
        "FAIL",
        "FILTER",
        "FIRST",
        "FOLLOWING",
        "FOR",
        "FOREIGN",
        "FROM",
        "FULL",
        "GENERATED",
        "GLOB",
        "GROUP",
        "GROUPS",
        "HAVING",
        "IF",
        "IGNORE",
        "IMMEDIATE",
        "IN",
        "INDEX",
        "INDEXED",
        "INITIALLY",
        "INNER",
        "INSERT",
        "INSTEAD",
        "INTERSECT",
        "INTO",
        "IS",
        "ISNULL",
        "JOIN",
        "KEY",
        "LAST",
        "LEFT",
        "LIKE",
        "LIMIT",
        "MATCH",
        "MATERIALIZED",
        "NATURAL",
        "NO",
        "NOT",
        "NOTHING",
        "NOTNULL",
        "NULL",
        "NULLS",
        "OF",
        "OFFSET",
        "ON",
        "OR",
        "ORDER",
        "OTHERS",
        "OUTER",
        "OVER",
        "PARTITION",
        "PLAN",
        "PRAGMA",
        "PRECEDING",
        "PRIMARY",
        "QUERY",
        "RAISE",
        "RANGE",
        "RECURSIVE",
        "REFERENCES",
        "REGEXP",
        "REINDEX",
        "RELEASE",
        "RENAME",
        "REPLACE",
        "RESTRICT",
        "RETURNING",
        "RIGHT",
        "ROLLBACK",
        "ROW",
        "ROWS",
        "SAVEPOINT",
        "SELECT",
        "SET",
        "TABLE",
        "TEMP",
        "TEMPORARY",
        "THEN",
        "TIES",
        "TO",
        "TRANSACTION",
        "TRIGGER",
        "UNBOUNDED",
        "UNION",
        "UNIQUE",
        "UPDATE",
        "USING",
        "VACUUM",
        "VALUES",
        "VIEW",
        "VIRTUAL",
        "WHEN",
        "WHERE",
        "WINDOW",
        "WITH",
        "WITHOUT",
    }

    @classmethod
    def __prepare__(mcls, name, base) -> Any | dict:
        """
        Prepare the class dictionary with keywords and their corresponding colors.
        :param mcls: The metaclass.
        :param name: The name of the class.
        :param base: The base class.
        :return: A dictionary containing keywords and their colors.
        :rtype: Any | dict

        """
        cls_dict: dict = super().__prepare__(mcls, name, base)
        keywords: dict = dict()

        for keyword, color in zip(mcls.keywords, cycle(("magenta4",))):
            keywords[keyword] = color

        for punctuation, color in zip(string.punctuation, cycle(("steel blue",))):
            keywords[punctuation] = color

        for number, color in zip(range(10), cycle(("blue4",))):
            keywords[str(number)] = color

        keywords[";"] = "gray26"

        cls_dict["keywords_dict"] = keywords
        cls_dict["keywords_set"] = mcls.keywords
        return cls_dict

    def __new__(mcls, name, bases, namespace) -> Self:
        """
        Create a new class instance.

        :param mcls: The metaclass.
        :param name: The name of the class.
        :param bases: The base classes.
        :param namespace: The namespace containing class attributes.
        :return: A new instance of the class.
        :rtype: Self

        """
        return super().__new__(mcls, name, bases, namespace)
