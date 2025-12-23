import re


class Emails(list):
    def __init__(self, emails):
        self.validate(emails)

        unique_emails = list(set(emails))
        super().__init__(unique_emails)
        self.data = unique_emails

    def validate(self, emails):
        if not isinstance(emails, list):
            raise ValueError

        email_regex = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )

        for email in emails:
            if not isinstance(email, str):
                raise ValueError
            if not email_regex.match(email):
                raise ValueError

    def __repr__(self):
        return f"Emails({list(self)})"

    def __str__(self):
        return "\n".join(self)
