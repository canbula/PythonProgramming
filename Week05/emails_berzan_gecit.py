import re


class Emails(list):

    _pattern = re.compile(r"[\w.+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+")

    def __init__(self, emails=None):
        super().__init__()
        emails = [] if emails is None else list(emails)
        self.validate(emails)
        for email in emails:
            if email not in self:
                self.append(email)

    @property
    def data(self):
        return self

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("Emails must be strings")
            if not self._pattern.fullmatch(email):
                raise ValueError(f"Invalid email address: {email}")

    def __repr__(self):
        return f"Emails({list.__repr__(self)})"

    def __str__(self):
        return ", ".join(self)
