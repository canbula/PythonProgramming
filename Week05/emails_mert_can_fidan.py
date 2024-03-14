import re

class Emails(list):
    def __init__(self, data: [str]) -> None:
        self.data = list(set(data))
        self.validate(data)
        
    def __repr__(self):
        return f"Emails({self.data})"
    
    def __str__(self):
        return f"Emails: {self.data}"
        
    def validate(self, data: [str]) -> None:
        # Validate email addresses according to the pattern used by Gmail.
        # The local part (before the @) can contain:
        # - Alphanumeric characters
        # - Periods (.) but not consecutively or at the start/end
        # The domain part (after the @) can contain:
        # - Alphanumeric characters
        # - Periods (.) followed by at least two alphabetic characters
        # This pattern also supports subdomains.
        regex_pattern = r"^[A-Za-z0-9]+(?:[.][A-Za-z0-9]+)*@[A-Za-z0-9]+(?:\.[A-Za-z]{2,}){1,2}$"

        for email in data:
            if isinstance(email, int):
                raise ValueError("Only string values accepted!")
            if not re.match(regex_pattern, email):
                raise ValueError(f"Invalid email format: {email}") 
