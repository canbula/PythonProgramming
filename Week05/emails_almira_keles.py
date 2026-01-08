from __future__ import annotations

import re
from typing import Iterable, List


_EMAIL_RE = re.compile(
    # Basit ama yeterli doğrulama:
    # local@domain.tld (en az bir nokta içeren domain)
    r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
)


class Emails(list):
    """
    A list-like container that stores validated, unique email addresses.
    - Accepts an iterable of emails on init.
    - Validates: items must be strings and must look like valid emails.
    - Removes duplicates (keeps first occurrence).
    - Stores the final list in self.data as well.
    """

    def __init__(self, emails: Iterable[str]):
        # list subclass init
        super().__init__()
        self.data: List[str] = self.validate(emails)
        # keep list content consistent with .data
        self.extend(self.data)

    @staticmethod
    def validate(emails: Iterable[str]) -> List[str]:
        # Iterable kontrolü: testler liste gönderiyor ama genel olsun.
        if emails is None:
            raise ValueError("Emails cannot be None")

        unique: List[str] = []
        seen = set()

        for item in emails:
            if not isinstance(item, str):
                raise ValueError("All email addresses must be strings")

            email = item.strip()
            if not _EMAIL_RE.match(email):
                raise ValueError(f"Invalid email address: {item}")

            # duplicate engelle (case-sensitive bırakıyorum; test bunu zorlamıyor)
            if email not in seen:
                seen.add(email)
                unique.append(email)

        return unique

    def __repr__(self) -> str:
        # Testin beklediği kritik nokta:
        # repr(obj) == obj.__repr__()
        # ayrıca "reproduce" teması: Emails([...]) biçiminde üretilebilir.
        return f"Emails({self.data!r})"

    def __str__(self) -> str:
        # İnsan okunur: virgülle birleştir
        return ", ".join(self.data)
Footer
