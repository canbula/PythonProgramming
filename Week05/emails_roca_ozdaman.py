import re

class Emails(list):
    def __init__(self, emails):
        self.validate(emails)
        self.data = list(set(emails))
        super().__init__(self.data)

    def validate(self, emails):
        if not all(isinstance(e, str) for e in emails):
            raise ValueError("All items must be strings")

        pattern = r"^[^@]+@[^@]+\.[^@]+$"

        for email in emails:
            if not re.match(pattern, email):
                raise ValueError("Invalid email address")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"

    def __str__(self):
        return ", ".join(self.data)
