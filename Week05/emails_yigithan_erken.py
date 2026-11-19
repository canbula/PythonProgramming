class Emails(list):
    def __init__(self, initial_emails=None):
        super().__init__()
        self.data = self
        if initial_emails is not None:
            self.validate(initial_emails)

    def validate(self, emails_to_check):
        for item in emails_to_check:
            if not isinstance(item, str):
                raise ValueError("List can only contain strings")
            
            if "@" not in item:
                raise ValueError("Invalid email format")
                
            domain_part = item.split("@")[1]
            if "." not in domain_part:
                raise ValueError("Invalid email format")
            
            if item not in self:
                self.append(item)

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return super().__str__()