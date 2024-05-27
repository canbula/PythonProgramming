
class Emails(list):
    def __init__(self, addresses: list):
        for i, address in enumerate(addresses):
            if not self.validate(address):
                raise ValueError(f"invalid address {address!r} at index {i}")
        super().__init__(set(addresses))

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self):
        return super().__str__()

    @property
    def data(self):
        return self

    @staticmethod
    def validate(address: str) -> bool:
        if not isinstance(address, str):
            raise ValueError("address must be a str")
        return "@" in address and "." in address
