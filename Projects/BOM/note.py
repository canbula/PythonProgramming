from db import Firebase
from user import User

class Note:
    def __init__(self, user_id: str, f: Firebase) -> None:
        self.note_id = ""
        self.user_id = user_id
        self.title = ""
        self.description = ""
        self.note_idf = self.note_id
        self.ref = f.ref.child("notes").child(user_id)  # Reference to notes under the user
        self.user = User(user_id, f)

    def create(self):
        # Generate a new unique ID by pushing to the user's notes reference
        new_note_ref = self.ref.push(
            {
                "title": self.title,
                "description": self.description,
                "user_id": self.user_id,
                "note_idf": self.note_idf
                
            }
        )
        self.note_id = new_note_ref.key
        self.note_idf = self.note_id
        return self

    def save(self):
        if not self.note_id:
            raise ValueError("Note ID is not set. Cannot save note.")
        self.ref.child(self.note_id).set(
            {
                "title": self.title,
                "description": self.description,
                "user_id": self.user_id,
                "note_idf": self.note_idf
            }
        )
        return self

    def update(self, updates: dict = {}):
        if updates:
            self.title = updates.get("title", self.title)
            self.description = updates.get("description", self.description)
        self.save()
        return self

    def get(self, note_id: str):
        if not note_id:
            raise ValueError("Note ID is not provided.")
        self.note_id = note_id
        note_ref = self.ref.child(note_id)
        note = note_ref.get()
        if not note:
            raise ValueError(f"Note with ID {note_id} does not exist.")
        self.title = note.get("title", "")
        self.description = note.get("description", "")
        self.note_idf = note.get("note_idf", "")
        return note

    def delete(self):
        if not self.note_id:
            raise ValueError("Note ID is not set. Cannot delete note.")
        self.ref.child(self.note_id).delete()
        self.title = ""
        self.note_idf = ""
        self.description = ""
        self.note_id = ""
        return self

    def __str__(self):
        return f"{self.title} - {self.description} by {self.user.department} {self.user.fullname}"
