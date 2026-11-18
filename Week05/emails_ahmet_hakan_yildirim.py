import re

PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}"


class Emails(list):
    def __init__(self, addresses: list) -> None:
        self.data = self.validate(addresses)
        list.__init__(self, self.data)

    @classmethod
    def validate(cls, addresses: list) -> list:
        if not all(isinstance(a, str) for a in addresses):
            raise ValueError("All e-mail addresses must be strings")
        for a in addresses:
            if re.fullmatch(PATTERN, a) is None:
                raise ValueError(f"Not a valid e-mail address: {a}")
        # dict.fromkeys removes duplicates and keeps the order
        return list(dict.fromkeys(addresses))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __str__(self) -> str:
        return f"{len(self.data)} e-mail(s): " + " | ".join(self.data)
