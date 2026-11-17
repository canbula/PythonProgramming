class Emails(list):
    def __init__(self, iterable=()):
        validated_emails = self._filter_and_validate(iterable)
        super().__init__(validated_emails)
        self.data = list(self)

    @staticmethod
    def _is_valid_address(email: str) -> bool:
        if email.count("@") != 1:
            return False
        local, domain = email.split("@")
        if not local or not domain or "." not in domain:
            return False
        if domain.startswith(".") or domain.endswith("."):
            return False
        return True

    def _filter_and_validate(self, raw_emails):
        unique_emails = []
        seen = set()
        for addr in raw_emails:
            if not isinstance(addr, str):
                raise ValueError("Only strings are allowed")
            if not self._is_valid_address(addr):
                raise ValueError(f"Invalid email: {addr}")
            if addr not in seen:
                seen.add(addr)
                unique_emails.append(addr)
        return unique_emails

    def __repr__(self):
        return f"Emails({super().__repr__()})"

    def __str__(self):
        lines = [f"{idx}. {addr}" for idx, addr in enumerate(self, 1)]
        return "Emails:\n" + "\n".join(lines) + ("\n" if lines else "")