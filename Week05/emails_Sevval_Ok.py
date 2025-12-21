import re
from typing import Iterable, List

class Emails(list)
    _EMAIL_RE = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    @classmethod
    def validate(cls, items: Iterable) -> List[str]:
        cleaned = []
        for it in items:
            if not isinstance(it, str):
                raise ValueError
            if not cls._EMAIL_RE.match(it):
                raise ValueError
            cleaned.append(it)
        return cleaned

    def __init__(self, items):
        validated = self.validate(items)

        unique = list(dict.fromkeys(validated))

        self.data = unique  # tests check .data.count(...)
        super().__init__(unique)

    def __repr__(self) -> str:       
        return f"{self.__class__.__name__}({self.data!r})"

    def __str__(self) -> str:
        return ", ".join(self.data)
