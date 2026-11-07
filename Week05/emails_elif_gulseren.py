import re

class Emails(list):
    def __init__(self, emails=None):
        if emails is None:
            emails = []
            
        valid_emails = []
        for email in emails:
            if self.validate(email):
                if email not in valid_emails:
                    valid_emails.append(email)
                    
        super().__init__(valid_emails)
        
        self.data = self

    def validate(self, email):
        if not isinstance(email, str):
            raise ValueError("Bütün e-posta adresleri metin (string) formatında olmalıdır.")
        
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise ValueError(f"Geçersiz e-posta formatı: {email}")
            
        return True

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()
