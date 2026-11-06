import re


class Emails(list):
    """A list of unique and valid email addresses."""

    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

    def __init__(self, emails):
        self.data = self.validate(emails)
        super().__init__(self.data)

    def validate(self, emails):
        """
        Check the given email addresses and remove the duplicates.

        :param emails: The email addresses to validate
        :raises ValueError: If an item is not a string or not a valid email address
        :return: A list of unique email addresses in their original order
        """
        unique_emails = []
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"{email!r} is not a string")
            if not self.EMAIL_PATTERN.match(email):
                raise ValueError(f"{email!r} is not a valid email address")
            if email not in unique_emails:
                unique_emails.append(email)
        return unique_emails

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)
