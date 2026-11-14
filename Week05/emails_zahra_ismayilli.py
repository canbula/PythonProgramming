import re


class Emails(list):

    def __init__(self, emails=None):
        super().__init__()

        if emails is None:
            emails = []

        for email in emails:
            self.validate(email)

            if email not in self:
                self.append(email)

        self.data = self

    @staticmethod
    def validate(email):
        if not isinstance(email, str):
            raise ValueError("Email must be a string")

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        if re.fullmatch(pattern, email) is None:
            raise ValueError("Invalid email address")

        return True

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return str(list(self))
