class Emails(list):
    def __init__(self, emails):
        validated = self.validate(emails)
        super().__init__(validated)
        self.data = validated

    def validate(self, emails):
        unique = []
        for email in emails:
            if not isinstance(email, str):
                raise ValueError(f"Email must be a string: {email!r}")
            if email.count("@") != 1:
                raise ValueError(f"Invalid email address: {email}")
            user, domain = email.split("@")
            if user == "" or "." not in domain:
                raise ValueError(f"Invalid email address: {email}")
            if domain.startswith(".") or domain.endswith("."):
                raise ValueError(f"Invalid email address: {email}")
            if email not in unique:
                unique.append(email)
        return unique

    def __repr__(self):
        return f"Emails({self.data!r})"

    def __str__(self):
        return ", ".join(self.data)
