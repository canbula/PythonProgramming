class Emails(list):
    """
    A custom list class for storing and validating email addresses.
    Inherits from the built-in list class.
    """

    def __init__(self, emails_list):
        """
        Initializes the Emails object with a list of email addresses.
        Validates each email and prevents duplicate entries.
        """
        super().__init__()
        
        self.data = self

        for email in emails_list:

            if not isinstance(email, str):
                raise ValueError("All elements must be of type string.")

            if not self.validate(email):
                raise ValueError("Invalid email address format.")

            if email not in self:
                self.append(email)

    def validate(self, email: str) -> bool:
        """
        Validates the email format.
        An email is considered valid if it contains an '@' symbol
        and a '.' in the domain part (after the '@').
        """
        if "@" in email:
            domain_part = email.split("@")[-1]
            if "." in domain_part:
                return True
        return False

    def __repr__(self):
        """
        Returns the official string representation of the Emails object.
        """
        return super().__repr__()

    def __str__(self):
        """
        Returns the user-friendly string representation of the Emails object.
        """
        return super().__str__()