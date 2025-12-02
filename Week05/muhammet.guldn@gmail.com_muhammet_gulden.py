# emails_isim_soyisim.py
import re

class Emails(list):
    def __init__(self, email_list):
        self.validate(email_list)
        
        unique_emails = []
        for email in email_list:
            if email not in unique_emails:
                unique_emails.append(email)
        
        self.data = unique_emails
        
        super().__init__(unique_emails)
    
    def validate(self, email_list):
        """Email listesini validate eder"""
        for email in email_list:
            if not isinstance(email, str):
                raise ValueError(f"{email} is not a string")
            
            if '@' not in email or '.' not in email:
                raise ValueError(f"{email} is not a valid email address")
            
            if email.index('@') > email.rindex('.'):
                raise ValueError(f"{email} is not a valid email address")
    
    def __repr__(self):
        """repr() fonksiyonu için"""
        return f"Emails({self.data})"
    
    def __str__(self):
        """print() için"""
        return f"Emails({self.data})"
