import re


class Emails(list):
    """
    This class keeps a list of unique and valid email addresses.
    """

    def __init__(self, emails: list) -> None:
        super().__init__(self.validate(emails))

    @property
    def data(self) -> "Emails":
        """
        This property returns the email addresses.
        """
        return self

    @staticmethod
    def validate(emails: list) -> list:
        """
        This method checks the email addresses and removes the duplicates.
        """
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"{email!r} is not a string")
            if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email):
                raise ValueError(f"{email!r} is not a valid email address")
        return list(dict.fromkeys(emails))

    def __repr__(self) -> str:
        return f"Emails({list(self)!r})"

    def __str__(self) -> str:
        return ", ".join(self)
