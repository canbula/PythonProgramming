import re


class Emails(list):
    """A list of unique, validated email addresses."""

    def __init__(self, emails):
        unique = []
        for email in emails:
            self.validate(email)
            if email not in unique:
                unique.append(email)
        super().__init__(unique)

    @property
    def data(self):
        return self

    @staticmethod
    def validate(email):
        if not isinstance(email, str):
            raise ValueError("Email addresses must be strings")
        if re.fullmatch(r"[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+", email) is None:
            raise ValueError("Invalid email address")
        return True

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return ", ".join(self)
