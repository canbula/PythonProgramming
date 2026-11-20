class Emails(list):
    def __init__(self, emails=[]):
        clean_email_list = self.validate(emails)
        super().__init__(clean_email_list)
        self.data = self

    def validate(self, emails):
        unique_emails = []
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("The email must be a string!")
            if email.count('@') != 1:
                raise ValueError("Invalid email format. There can't be more than 1 @ symbol!")
            name, domain = email.split('@')
            if not name:
                raise ValueError("Invalid email format. The part before the @ (the name) is missing!")
            if not domain:
                raise ValueError("Invalid email format. The part after the @ (the domain) is missing!")
            if '.' not in domain:
                raise ValueError("Invalid email format. The part after the @ (the domain) is missing it's dot!")
            if domain.startswith('.') or domain.endswith('.'):
                raise ValueError("Invalid email format.")
            if email not in unique_emails:
                unique_emails.append(email)
        return unique_emails

    def __repr__(self):
        return f"Emails({list(self)})"

    def __str__(self):
        return ", ".join(self)

