class Emails(list):
    def __init__(self, email_list):
        valid_emails = self.validate(email_list)
        super().__init__(valid_emails)
        self.data = list(self)

    def validate(self, email_list):
        valid_list = []
        for item in email_list:
            if not isinstance(item, str):
                raise ValueError("Only strings are allowed")
            if item.count("@") != 1:
                raise ValueError("Invalid email: " + item)

            local_part, domain_part = item.split("@")
            if not local_part or "." not in domain_part:
                raise ValueError("Invalid email: " + item)
            if domain_part.startswith(".") or domain_part.endswith("."):
                raise ValueError("Invalid email: " + item)

            if item not in valid_list:
                valid_list.append(item)
        return valid_list

    def __repr__(self):
        return f"Emails({list(self)})"

    def __str__(self):
        lines = "Emails:\n"
        for index, email in enumerate(self, start=1):
            lines += f"{index}. {email}\n"
        return lines