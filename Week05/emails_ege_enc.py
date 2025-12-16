class Emails(list):
    def __init__(self, emails_list):
        self.validate(emails_list)
        unique_emails = list(dict.fromkeys(emails_list))
        super().__init__(unique_emails)
        self.data = self

    def validate(self, emails_list):
        for email in emails_list:
            if not isinstance(email, str):
                raise ValueError
            
            if "@" not in email:
                raise ValueError
            
            parts = email.split("@")
            if len(parts) != 2 or "." not in parts[1]:
                raise ValueError

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return super().__str__()
