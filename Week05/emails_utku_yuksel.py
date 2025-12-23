class Emails(list):
    def __init__(self, emails):
        self.validate(emails)
        unique_emails = []
        for email in emails:
            if email not in unique_emails:
                unique_emails.append(email)
        super().__init__(unique_emails)
        self.data = self

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError
            if "@" not in email or "." not in email:
                raise ValueError

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return super().__str__()
