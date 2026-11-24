import re


class Emails(list):
    PATTERN = r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$"

    def __init__(self, emails=()):
        super().__init__()
        self.data = self

        for email in emails:
            if not self.validate(email):
                raise ValueError(f"Invalid e-mail address: {email!r}")
            if email not in self:
                self.append(email)

    @staticmethod
    def validate(email):
        return isinstance(email, str) and re.match(Emails.PATTERN, email) is not None

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return ", ".join(self)
