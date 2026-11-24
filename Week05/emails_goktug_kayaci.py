import re


class Emails(list):

    def __init__(self, emails):
        self.data = []

        for email in emails:
            self.validate(email)

            if email not in self.data:
                self.data.append(email)

        super().__init__(self.data)

    def validate(self, email):
        if not isinstance(email, str):
            raise ValueError("Email must be a string")

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(pattern, email):
            raise ValueError("Invalid email address")

        return True

    def __repr__(self):
        return f"Emails({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)
