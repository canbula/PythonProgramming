class Emails(list):

    def __init__(self, emails=None):
        super().__init__()
        self.data = self

        if emails is not None:
            self.validate(emails)

    def validate(self, emails):

        for email in emails:

            if not isinstance(email, str):
                raise ValueError("Email must be a string")

            if "@" not in email:
                raise ValueError("Invalid email")

            parts = email.split("@")

            if len(parts) != 2 or parts[0] == "":
                raise ValueError("Invalid email")

            domain = parts[1]

            if "." not in domain:
                raise ValueError("Invalid email")

            if domain.startswith(".") or domain.endswith("."):
                raise ValueError("Invalid email")

            if email not in self:
                self.append(email)

    def __repr__(self):
        return "Emails(" + repr(list(self)) + ")"

    def __str__(self):
        return str(list(self))
