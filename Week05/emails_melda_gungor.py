class Emails(list):
    def __init__(self, emails=None):
        if emails is None:
            emails = []

        valid_unique_emails = []
        for email in emails:
            self.validate(email)
            if email not in valid_unique_emails:
                valid_unique_emails.append(email)


        super().__init__(valid_unique_emails)
        self.data = self

    @staticmethod
    def validate(email):
        if not isinstance(email, str):
            raise ValueError(f"email must be a string, got {type(email)}")
        if email.count("@") != 1:
            raise ValueError(f"invalid email address: {email}")

        user, domain = email.split("@")

        if not user or not domain:
            raise ValueError(f"invalid email address: {email}")

        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError(f"invalid email address: {email}")
        
        return True 

    def __repr__(self):
        return f"Emails({list(self)})"

    def __str__(self):
        return super().__str__()

