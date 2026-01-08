class Emails(list):
    def __init__(self, emails=None):
        super().__init__()

        if emails is None:
            return

        for email in emails:
            if isinstance(email, str) and "@" in email:
                email = email.lower()
                if email not in self:
                    self.append(email)
