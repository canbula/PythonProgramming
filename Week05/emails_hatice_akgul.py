import re

class Emails(list):
    """
    Emails class that extends list and validates email addresses.
    """
    def __init__(self, email_list):
        validated_data = self.validate(email_list)
        super().__init__(validated_data)
        self.data = list(validated_data)

    @staticmethod
    def validate(email_list):
        """
        Validates that all items are strings and follow email format.
        Removes duplicates while preserving order (or just unique set).
        """
        seen = []
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for email in email_list:
            if not isinstance(email, str):
                raise ValueError("All items must be strings.")
            
            if not re.match(email_regex, email):
                raise ValueError(f"Invalid email format: {email}")
            
            if email not in seen:
                seen.append(email)
                
        return seen

    def __repr__(self):
        """
        Returns a string representation that can recreate the object.
        """
        return f"Emails({list(self)})"

    def __str__(self):
        """
        Returns a user-friendly string representation.
        """
        return f"Email List: {list(self)}"
