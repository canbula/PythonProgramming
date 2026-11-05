
import re


class Emails(list):
    """A list of unique and valid email addresses."""

    EMAIL_PATTERN = re.compile(
        r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$"
    )

    def __init__(self, emails):
        valid_emails = self.validate(emails)
        super().__init__(valid_emails)
        self.data = list(self)

    @staticmethod
    def validate(emails):
        unique_emails = []

        for email in emails:
            if not isinstance(email, str):
                raise ValueError("Email must be a string")

            if not Emails.EMAIL_PATTERN.fullmatch(email):
                raise ValueError("Invalid email address")

            if email not in unique_emails:
                unique_emails.append(email)

        return unique_emails

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return ", ".join(self)
