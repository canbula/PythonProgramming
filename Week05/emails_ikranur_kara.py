import re

class Emails(list):
    def __init__(self, email_list=None):
        if email_list is None:
            email_list = []
        
        valid_emails = []
        for email in email_list:
            self.validate(email)
            if email not in valid_emails:
                valid_emails.append(email)
                
        super().__init__(valid_emails)

    @staticmethod
    def validate(email):
        if not isinstance(email, str):
            raise ValueError("Email must be a string.")
        
        # Basit e-posta doğrulama: kullanıcı_adı@domain.uzantı
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(pattern, email):
            raise ValueError(f"Invalid email address: {email}")

    @property
    def data(self):
        return list(self)

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return f"Emails: {super().__str__()}"
