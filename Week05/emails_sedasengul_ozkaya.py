import re

class Emails(list):
    def __init__(self, initial_data=None):
        super().__init__()
        self.data = self
        
        if initial_data is not None:
            for item in initial_data:
                if not isinstance(item, str):
                    raise ValueError()
                
                if not self.validate(item):
                    raise ValueError()
                
                if item not in self:
                    self.append(item)

    @staticmethod
    def validate(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, str(email)))

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        return super().__str__()
