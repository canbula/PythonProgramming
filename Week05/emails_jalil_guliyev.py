"""Week 05: Emails homework."""

import re


class Emails(list):
    """A list of unique, validated email addresses."""

    _EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$")

    def __init__(self, emails):
        validated = self.validate(emails)
        super().__init__(validated)
        self.data = self

    @classmethod
    def validate(cls, emails):
        """Validate addresses and return unique values in input order."""
        unique = []
        for email in emails:
            if not isinstance(email, str) or not cls._EMAIL_PATTERN.fullmatch(email):
                raise ValueError(f"Invalid email address: {email!r}")
            if email not in unique:
                unique.append(email)
        return unique

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return f"Emails({list(self)!r})"
