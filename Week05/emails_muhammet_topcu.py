import re

class Emails(list):
    def __init__(self, emails):
        self.validate(emails)
        unique = []
        for e in emails:
            if e not in unique:
                unique.append(e)
        super().__init__(unique)
        self.data = unique

    @staticmethod
    def validate(emails):
        if not all(isinstance(e, str) for e in emails):
            raise ValueError("emails must be strings")
        pattern = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
        for e in emails:
            if not pattern.match(e):
                raise ValueError("invalid email")

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"

    def __str__(self):
        return ", ".join(self)
