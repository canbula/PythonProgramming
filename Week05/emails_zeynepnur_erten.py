class Emails(list):
    def __init__(self, emails_list):
        checked_emails = self.validate(emails_list)
        super().__init__(checked_emails)
        self.data=checked_emails


    def validate(self,emails_list):
       validated_emails = []
       for email in emails_list:
           if not isinstance(email, str):
               raise ValueError('emails must be a string')
           if "@" not in email or "." not in email:
               raise ValueError('emails must start with @ and must end with .')
           if email not in validated_emails:
               validated_emails.append(email)
       return validated_emails

    def __repr__(self):
        return f"Emails( {str(list(self))} )"
    def __str__(self):
        result = "Emails: \n"
        for i in self.data:
            result += f"{i} \n"
        return result
