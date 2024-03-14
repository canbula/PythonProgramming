class Emails(list):
    def __init__(self, data: [str]) -> None:
        self.data = list(set(data))
        self.validate(data)
        
    def __repr__(self):
        return f"Emails({self.data})"
    
    def __str__(self):
        return f"Emails: {self.data}"
        
    def validate(self, data: [str]) -> None:
        for email in data:
            if isinstance(email, int):
                raise ValueError("Only string values accepted!")
            if "@" not in email:
                raise ValueError("This is not an email adress!")
