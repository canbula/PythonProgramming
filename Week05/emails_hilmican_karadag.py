import re


class Emails(list):

    EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    def __init__(self, emails):
        super().__init__()
        self.validate(emails)
        for email in emails:
            if email not in self:  # tekrar edenleri ekleme
                self.append(email)

    @property
    def data(self):
        return list(self)

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"{email!r} is not a string")
            if not self.EMAIL_PATTERN.fullmatch(email):
                raise ValueError(f"{email!r} is not a valid email address")

    def __repr__(self):
        return f"Emails({list.__repr__(self)})"

    def __str__(self):
        return ", ".join(self)