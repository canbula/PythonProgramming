import re


# Class to store unique and valid email addresses
class Emails(list):
    def __init__(self, emails):
        # Validate emails and save them
        valid = self.validate(emails)
        super().__init__(valid)
        self.data = valid

    def validate(self, emails):
        clean_list = []
        pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        for item in emails:
            # Check if item is a string
            if not isinstance(item, str):
                raise ValueError("Email must be a string")
            # Check if email format is valid
            if not re.match(pattern, item):
                raise ValueError("Invalid email address")
            # Add only unique emails
            if item not in clean_list:
                clean_list.append(item)

        return clean_list

    def __repr__(self):
        # Return code representation of the object
        return f"Emails({list(self)})"

    def __str__(self):
        # Return readable string of emails
        return "\n".join(self)
