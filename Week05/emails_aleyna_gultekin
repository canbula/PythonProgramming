import re


class Emails(list):
    """A list of unique and valid e-mail addresses."""

    EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, emails):
        valid_emails = self.validate(emails)
        super().__init__(valid_emails)
        self.data = list(self)

    @staticmethod
    def validate(emails):
        unique = []
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"{email!r} is not a string")
            if not Emails.EMAIL_PATTERN.match(email):
                raise ValueError(f"{email!r} is not a valid e-mail address")
            if email not in unique:
                unique.append(email)
        return unique

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return ", ".join(self)
