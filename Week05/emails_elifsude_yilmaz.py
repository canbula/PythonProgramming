import re


class Emails(list):
    def __init__(self, data):
        self.data = []
        self.validate(data)
        super().__init__(self.data)

    def validate(self, data):
        # only list input
        if not isinstance(data, list):
            raise ValueError("Input must be a list")

        email_pattern = re.compile(
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        seen = set()

        for item in data:
            # allow only strings
            if not isinstance(item, str):
                raise ValueError("All emails must be strings")

            # valid email check
            if not email_pattern.match(item):
                raise ValueError("Invalid email address")

            # remove duplicates
            if item not in seen:
                seen.add(item)
                self.data.append(item)

    def __repr__(self):
        return f"Emails({self.data})"

    def __str__(self):
        return ", ".join(self.data)
