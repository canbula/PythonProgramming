import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class Emails(list):
    @staticmethod
    def validate(email_list):
        if not all(isinstance(mail, str) for mail in email_list):
            raise ValueError("Emails list can only contain string values.")

        for mail in email_list:
            if not re.fullmatch(EMAIL_REGEX, mail):
                raise ValueError(f"'{mail}' is not a valid email format.")

        return list(set(email_list))

    def __init__(self, initial_emails=None):
        initial_emails = initial_emails or []
        clean_list = Emails.validate(initial_emails)
        self.data = clean_list
        super().__init__(clean_list)

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return "\n".join(self)
