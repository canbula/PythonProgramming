import re


class Emails(list):
    def __init__(self, emails=None):
        if emails is None:
            emails = []
        self.validate(emails)
        unique_emails = list(dict.fromkeys(emails))
        self.data = unique_emails
        super().__init__(unique_emails)

    @staticmethod
    def validate(emails):
        if not isinstance(emails, (list, tuple, set)):
            raise ValueError("Emails must be provided in a list")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("All emails must be strings")
            if not re.match(pattern, email):
                raise ValueError(f"Invalid email address: {email}")

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return ", ".join(self)