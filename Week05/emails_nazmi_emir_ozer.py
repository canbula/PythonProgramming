class Emails(list):
    def __init__(self, emails):
        self.validate(emails)
        self.data = list(dict.fromkeys(emails))
        super().__init__(self.data)

    def validate(self, emails):
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("Email must be a string: " + repr(email))
            if email.count("@") != 1:
                raise ValueError("Invalid email address: " + email)
            local, domain = email.split("@")
            if local == "" or "." not in domain:
                raise ValueError("Invalid email address: " + email)
            if any(part == "" for part in domain.split(".")):
                raise ValueError("Invalid email address: " + email)

    def __repr__(self):
        return "Emails(" + repr(self.data) + ")"

    def __str__(self):
        return ", ".join(self.data)