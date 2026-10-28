class Emails(list):
    def __init__(self, email_list):
        checked = self.validate(email_list)
        super().__init__(checked)
        self.data = checked

    def validate(self, email_list):
        result = []
        for item in email_list:
            if type(item) is not str:
                raise ValueError("Only strings are allowed")
            if item.count("@") != 1:
                raise ValueError("Invalid email: " + item)
            user, domain = item.split("@")
            if user == "" or "." not in domain:
                raise ValueError("Invalid email: " + item)
            if domain.startswith(".") or domain.endswith("."):
                raise ValueError("Invalid email: " + item)
            if item not in result:
                result.append(item)
        return result

    def __repr__(self):
        return "Emails(" + str(list(self)) + ")"

    def __str__(self):
        text = "Emails:\n"
        for i, mail in enumerate(self, start=1):
            text += f"{i}. {mail}\n"
        return text
