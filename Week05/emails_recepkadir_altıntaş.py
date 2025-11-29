class Emails(list):
    def __init__(self, emails):
        unique_emails = []
        seen = set()
        for email in emails:
            if email not in seen:
                unique_emails.append(email)
                seen.add(email)

        self.validate(unique_emails)
        super().__init__(unique_emails)
        self.data = self

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("All items must be strings")

            if "@" not in email:
                raise ValueError("Email must contain @")

            parts = email.split("@")
            if len(parts) != 2 or "." not in parts[1]:
                raise ValueError("Invalid domain format")

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return super().__str__()
