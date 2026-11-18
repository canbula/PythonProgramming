import re


class Emails(list):
    """A list of unique, validated email addresses."""

    _pattern = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, emails):
        self.validate(emails)
        self.data = list(dict.fromkeys(emails))
        super().__init__(self.data)

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"{email!r} is not a string")
            if not self._pattern.match(email):
                raise ValueError(f"{email!r} is not a valid email address")

    def __repr__(self):
        return f"Emails({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)