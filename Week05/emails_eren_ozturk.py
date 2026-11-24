class Emails(list):
    def __init__(self, emails=None):
        if emails is None:
            emails = []
        self.validate(emails)
        unique_emails = []
        for email in emails:
            if email not in unique_emails:
                unique_emails.append(email)
        self.data = unique_emails
        super().__init__(unique_emails)

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("All elements must be strings.")
            if "@" not in email:
                raise ValueError("Invalid email address.")
            parts = email.split("@")
            if len(parts) != 2 or not parts[0] or "." not in parts[1]:
                raise ValueError("Invalid email address.")
            domain_parts = parts[1].split(".")
            if not domain_parts[0] or not domain_parts[-1]:
                raise ValueError("Invalid email address.")

    def __repr__(self):
        return f"Emails({self.data})"

    def __str__(self):
        return f"Emails: {self.data}"