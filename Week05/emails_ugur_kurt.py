import re


class Emails(list):
    """A list of unique, valid email addresses."""

    EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")

    def __init__(self, emails):
        validated = self.validate(emails)
        super().__init__(validated)
        self.data = validated

    @classmethod
    def validate(cls, emails):
        """Return the addresses without duplicates; raise ValueError if any is invalid."""
        unique = []
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"Email must be a string: {email!r}")
            if not cls.EMAIL_PATTERN.match(email):
                raise ValueError(f"Invalid email address: {email!r}")
            if email not in unique:
                unique.append(email)
        return unique

    def __repr__(self):
        return f"Emails({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)
