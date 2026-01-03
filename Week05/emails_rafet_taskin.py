import re

class Emails(list):
    def __init__(self, emails):
        unique_emails = []
        if emails:
            seen = set()
            for email in emails:
                if email not in seen:
                    unique_emails.append(email)
                    seen.add(email)
        
        super().__init__(unique_emails)
        self.data = self
    
        self.validate()

    def validate(self):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') # good enough regex
        for email in self:
            if not isinstance(email, str):
                raise ValueError("Emails must be strings")
            
            if not email_pattern.match(email):
                raise ValueError(f"Invalid email address: {email}")

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return f"Emails({super().__str__()})"
