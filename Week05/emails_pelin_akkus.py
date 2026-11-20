import re


class Emails(list):
    """A list that stores unique, valid email addresses."""

    def __init__(self, emails=None):
        super().__init__()
        self.data = self

        if emails is None:
            emails = []

        for email in emails:
            self.append(email)

    @staticmethod
    def validate(email):
        """Check an email address and raise ValueError if it is invalid."""
        if not isinstance(email, str):
            raise ValueError("Email must be a string")

        # Simple format check for username@domain.extension
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
        if not re.fullmatch(pattern, email):
            raise ValueError("Invalid email address")
        return True

    def append(self, email):
        self.validate(email)
        # Keep only one copy of each address.
        if email not in self:
            super().append(email)

    def __str__(self):
        return ", ".join(self)

    def __repr__(self):
        return f"Emails({list(self)!r})"
