import re


class Emails(list):
    def __init__(self, data):
        self.validate(data)
        # duplicate'leri kaldır
        unique = list(dict.fromkeys(data))
        super().__init__(unique)
        self.data = self

    def validate(self, data):
        # sadece string olmalı
        for item in data:
            if not isinstance(item, str):
                raise ValueError("All items must be strings")

        # basit ama yeterli email kontrolü
        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
        for email in data:
            if not re.match(email_pattern, email):
                raise ValueError("Invalid email address")

    def __repr__(self):
        return f"Emails({list(self)})"

    def __str__(self):
        return ", ".join(self)
