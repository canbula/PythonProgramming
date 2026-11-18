import re


class Emails(list):
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

    def __init__(self, emails):
        super().__init__()
        self.data = self.validate(emails)
        self.extend(self.data)

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("All items must be strings")
            if not self.EMAIL_PATTERN.match(email):
                raise ValueError(f"Invalid email address: {email}")
        return list(dict.fromkeys(emails))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)
