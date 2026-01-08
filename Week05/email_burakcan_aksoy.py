import re

class Emails(list):
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def __init__(self, items):
        self._check(items)
        cleaned = self._unique(items)
        super().__init__(cleaned)
        self.data = cleaned

    def _check(self, items):
        if not all(type(x) is str for x in items):
            raise ValueError("All items must be strings")

        for mail in items:
            if not self.EMAIL_REGEX.fullmatch(mail):
                raise ValueError("Invalid email address")

    @staticmethod
    def _unique(items):
        seen = []
        for x in items:
            if x not in seen:
                seen.append(x)
        return seen

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"

    def __str__(self):
        return "\n".join(self)
