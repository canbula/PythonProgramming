class Email:
    def __init__(self, sender, receiver, subject):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject

    def __str__(self):
        return f"From: {self.sender}, To: {self.receiver}, Subject: {self.subject}"

class MarketingEmail(Email):
    def __init__(self, sender, receiver, subject, campaign_name):
        super().__init__(sender, receiver, subject)
        self.campaign_name = campaign_name

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Campaign: {self.campaign_name}"

class SupportEmail(Email):
    def __init__(self, sender, receiver, subject, ticket_id):
        super().__init__(sender, receiver, subject)
        self.ticket_id = ticket_id

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Ticket ID: {self.ticket_id}"
