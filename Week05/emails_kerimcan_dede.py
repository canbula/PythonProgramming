class Emails(list):
    
    def validate(self):
        for email in self:
            if not isinstance(email, str):
                raise ValueError("Emails must be string.")
            if email.count("@") != 1:
                raise ValueError("Emails must contain one @.")
            if "." not in email.split("@")[1]:
                raise ValueError("Emails must contain a dot after @.")
        else:
            print("Validation is successfull.")
        

    def __init__(self, iterable=None):
        super().__init__(iterable if iterable is not None else [])
        try:
            self.validate()
        except ValueError as error:
            print(error)

        unique_emails = list(dict.fromkeys(self))
        super().clear()
        super().extend(unique_emails)

    def __repr__(self):
        return f"Email list : ({super().__repr__()})"

    def __str__(self):
        return f"Email list : {list(self)}"

    @property
    def data(self):
        return self
