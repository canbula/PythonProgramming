import re

class Emails(list):
    def __init__(self, emails):
        validated_emails = self.validate(emails)
        self.data = validated_emails
        super().__init__(validated_emails)

    @staticmethod
    def validate(emails):
        unique_emails = []
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("All items must be strings.")
            if not re.match(email_regex, email):
                raise ValueError(f"Invalid email address: {email}")
            if email not in unique_emails:
                unique_emails.append(email)
                
        return unique_emails

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"

    def __str__(self):
        return f"{self.data}"
