class Emails(list):
    def __init__(self, emails):
        self.data = self.validate(emails)
        super().__init__(self.data)

    def validate(self, emails):
        result = []
        for email in emails:
            if type(email) is not str:
                raise ValueError("Emails must be strings.")
            if email.count("@") != 1 or "." not in email.split("@")[1]:
                raise ValueError("Invalid email address.")
            if email not in result:
                result.append(email)
        return result

    def __repr__(self):
        return f"Emails({self.data})"

    def __str__(self):
        return ", ".join(self.data)
