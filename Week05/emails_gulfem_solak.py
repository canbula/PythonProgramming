import re


class Emails(list):
    def __init__(self, emails):
        self.validate(emails)
        self.data = list(dict.fromkeys(emails))   # tekrarları sil
        super().__init__(self.data)               # parent'ı başlat

    @staticmethod
    def validate(emails):
        pattern = r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$"
        for email in emails:
            if not isinstance(email, str):
                raise ValueError("All items must be strings")
            if not re.match(pattern, email):
                raise ValueError(f"Invalid e-mail address: {email}")

    def __repr__(self):
        return f"Emails({self.data!r})"           # eval(repr(x)) nesneyi yeniden oluşturur

    def __str__(self):
        return ", ".join(self.data)
