import re

class Emails(list):
    def __init__(self, emails):
        super().__init__(dict.fromkeys(emails))
        self.__dict__['data'] = self 
        self.validate(self)

    def validate(self, emails):
        regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        if not all(type(e) is str and regex.match(e) for e in emails):
            raise ValueError("List contains invalid or non-string emails.")

    __str__ = lambda self: str(list(self))
    __repr__ = lambda self: f"{type(self).__name__}({super(Emails, self).__repr__()})"
