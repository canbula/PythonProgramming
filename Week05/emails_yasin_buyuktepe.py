import re


class Emails(list):
    def __init__(self, emails):
        super().__init__(self.validate(emails))

    @staticmethod
    def validate(emails):
        unique = []
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("Emails must be strings")
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValueError(f"Invalid email address: {email}")
            if email not in unique:
                unique.append(email)
        return unique

    @property
    def data(self):
        return list(self)

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return ", ".join(self)
