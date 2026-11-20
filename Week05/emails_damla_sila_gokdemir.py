import re

class Emails(list):
    def __init__(self, email_list):
        super().__init__(self.validate(email_list))

    def validate(self, email_list):
        valid_emails = []
        pattern = r"[^@\s]+@[^@.\s]+(?:\.[^@.\s]+)+"

        for email in email_list:
            if not isinstance(email, str):
                raise ValueError("Email must be a string")

            if re.fullmatch(pattern, email) is None:
                raise ValueError(f"Invalid email address: {email}")

            if email not in valid_emails:
                valid_emails.append(email)

        return valid_emails

    @property
    def data(self):
        return list(self)

    def __repr__(self):
        return f"Emails({list(self)!r})"

    def __str__(self):
        return f"Emails: {list(self)}"
