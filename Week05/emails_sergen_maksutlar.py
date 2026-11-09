class EmailList(list):

    def __init__(self, emails=None):
        super().__init__()
        self.data = self

        if emails:
            self.check_emails(emails)

    def check_emails(self, email_list):

        for email in email_list:

            if not isinstance(email, str):
                raise ValueError("Only string values are allowed")

            if "@" not in email:
                raise ValueError("Email address is not valid")

            domain = email.split("@", 1)[1]

            if "." not in domain:
                raise ValueError("Email address is not valid")

            if email not in self:
                self.append(email)

    def __repr__(self):
        return f"EmailList({list.__repr__(self)})"

    def __str__(self):
        return list.__str__(self)
