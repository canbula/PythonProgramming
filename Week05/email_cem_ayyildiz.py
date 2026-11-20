
import re


class Emails(list):

    def __init__(self, emails):
        self.data = []

        for email in emails:
            if not isinstance(email, str):
                raise ValueError("Only strings are allowed")

            self.validate(email)

            if email not in self.data:
                self.data.append(email)

        super().__init__(self.data)

    @staticmethod
    def validate(email):
        if not isinstance(email, str):
            raise ValueError("Email must be a string")

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(pattern, email):
            raise ValueError("Invalid email address")

        return True

    def __repr__(self):
        return f"Emails({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)
