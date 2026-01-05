import re


class Emails(list):
    def __init__(self, emails):
        self.validate(emails)
        super().__init__(list(dict.fromkeys(emails)))
        self.data = self

    def validate(self, emails):
        if not all(isinstance(e, str) for e in emails):
            raise ValueError("All items must be strings")

        email_pattern = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
        for email in emails:
            if not email_pattern.match(email):
                raise ValueError("Invalid email address")

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"

    def __str__(self):
        return ", ".join(self)
