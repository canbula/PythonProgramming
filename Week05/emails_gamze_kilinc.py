import re


class Emails(list):
    """
    A list subclass that stores and validates email addresses.
    """

    def __init__(self, data):
        self.validate(data)
        # remove duplicates
        unique_emails = list(set(data))
        super().__init__(unique_emails)
        self.data = self  # testlerde .data kullanıldığı için

    def validate(self, data):
        # check all items are strings
        for item in data:
            if not isinstance(item, str):
                raise ValueError("All items must be strings")

        # email regex 
        email_pattern = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

        for email in data:
            if not email_pattern.match(email):
                raise ValueError("Invalid email address")

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"

    def __str__(self):
        return ", ".join(self)
