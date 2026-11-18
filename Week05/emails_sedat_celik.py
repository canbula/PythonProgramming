import re


class Emails(list):
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def __init__(self, emails=None):
        if emails is None:
            emails = []
        elif isinstance(emails, (str, bytes)) or not hasattr(emails, "__iter__"):
            raise ValueError("Input must be an iterable of email strings.")

        unique_emails = []
        for email in emails:
            self.validate(email)
            if email not in unique_emails:
                unique_emails.append(email)

        super().__init__(unique_emails)

    @property
    def data(self):
        return self

    @staticmethod
    def validate(email):
        if isinstance(email, (list, tuple, set)):
            for item in email:
                Emails.validate(item)
            return True

        if not isinstance(email, str) or not Emails.EMAIL_PATTERN.match(email):
            raise ValueError(f"Invalid email address: {email!r}")
        return True

    def append(self, email):
        self.validate(email)
        if email not in self:
            super().append(email)

    def extend(self, emails):
        for email in emails:
            self.append(email)

    def insert(self, index, email):
        self.validate(email)
        if email not in self:
            super().insert(index, email)

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self):
        return ", ".join(self)
