import re

class Emails(list):
    def __init__(self, data):
        self.validate(data)
        unique_emails = list(set(data))
        super().__init__(unique_emails)
        self.data = unique_emails

    def validate(self, data):
        if not all(isinstance(x, str) for x in data):
            raise ValueError("All items must be strings")

        pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

        for email in data:
            if not pattern.match(email):
                raise ValueError("Invalid email address")

    def __repr__(self):
        return f"Emails({list(self)})"

    def __str__(self):
        return "\n".join(self)
