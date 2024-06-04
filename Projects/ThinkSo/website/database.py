import json
import sys
import pyrebase
import firebase_admin
from firebase_admin import credentials, db
from website.models import User, Note

paths_windows = {
    "db_config": "config\db_config.json", 
    "service_account_key" : "config\serviceAccountKey.json"
}

paths_macos = {
    "db_config": "./config/db_config.json",
    "service_account_key": "./config/serviceAccountKey.json"
}

paths = paths_macos if sys.platform == "darwin" else paths_windows

config = json.load(open(paths["db_config"], "r"))
certificate_file_path = paths["service_account_key"]

firebase = pyrebase.initialize_app(config)

class Firebase:
    def __init__(self):
        global config
        self.config = config
        self.cred = credentials.Certificate(certificate_file_path)
        firebase_admin.initialize_app(
            self.cred,
            {
                "databaseURL": config["databaseURL"]
            },
        )
        self.ref_root = db.reference("/")
        self.ref_notes = db.reference("notes")
        self.ref_users = db.reference("users")
        
    # TAKES USER or NOTE as dictionary and convert them into Objects
    def make_obj(self, raw, _type:str):
        if raw is not None:
            if _type.lower() == "user":
                if "notes" not in raw.keys():
                    raw.update({"notes": []})
                return User(id=raw["id"], email=raw["email"], password=raw["password"], name=raw["name"], notes=raw["notes"])
            
            elif _type.lower() == "note":
                return Note(id=raw["id"], user_ids=raw["user_ids"], title=raw["title"], content=raw["content"])

            else:
                print("\n # # # ERROR IN database.py\make_obj() LINE 93\n # # # ERROR: INCORRECT _type VALUE\n # # Possible types are ['user', 'note']")
                return None
        else:
            print("\n # # # ERROR IN database.py\make_obj() LINE 93\n # # # ERROR: INCORRECT raw VALUE\n # # the 'raw' is equal to None")
            return None

    # GETS THE LAST ID FOR THE SELECTED ITEM TYPE
    def get_last_id(self, user_or_note="user"):
        if user_or_note == "user":
            users = self.ref_users.get()
            if users is not None and users[-1] is not None:
                return users[-1]["id"]
            return -1

        else:
            notes = self.ref_notes.get()
            print("!!! notes : ", notes)
            if notes is not None and len(notes) > 0:
                if type(notes) is dict:
                    return max(note["id"] for note in notes.values() if note is not None)
                elif type(notes) is list:
                    return max(note["id"] for note in notes if note is not None)
#            if notes is not None and notes[list(notes)[-1]] is not None:
#                return notes[list(notes)[-1]]["id"]
            return -1



# # # # # # # # # # # # #
#         NOTES         
      
    # ADD METHODS         
    def add_note(self, note_dictionary):
        self.add_note(note_dictionary["user_ids"], note_dictionary["title"], note_dictionary["content"])

    def add_note(self, user_ids, title, content=""):  # Default content to an empty string
        note_id = self.get_last_id("note") + 1
        note = Note(note_id, user_ids, title, content)
        for user_id in user_ids:
            x = self.ref_users.child(str(user_id)).child("notes").get()
            if x is None:
                self.ref_users.child(str(user_id)).child("notes").set([note_id])
            else:
                x.append(note_id)
                self.ref_users.child(str(user_id)).child("notes").set(x)
        self.ref_notes.child(str(note_id)).set(note.__dict__)


    # GET METHODS
    def get_notes_raw(self):
        return self.ref_notes.get()
    
    def get_note_raw(self, id):
        if self.ref_notes.get() is not None:
            print("note id : ", id)
            a = self.ref_notes.order_by_key().equal_to(str(id)).limit_to_first(1).get()            
            print("notes : ", a)
            if type(a) is list:
                a_1 = [elem for elem in a if elem is not None]
                v = a_1[0]
            else:
                k, v =a.popitem()
            
            return v
        else:
            return None
    
    def get_note(self, id):
        raw_note = self.get_note_raw(id)
        note = self.make_obj(raw_note, "note")
        return note

    def get_user_notes(self, uid):
        user_note_ids = self.get_user(uid).notes
        user_notes = [self.get_note(note_id) for note_id in user_note_ids]
        return user_notes
    
    

    def get_notes(self, note_ids=[], raw=False):
        all_notes = []
        print("ALDIM : ", note_ids)
        if note_ids == "all":
            print("GETTING ALL OF THE NOTES!")
            all_notes = self.get_notes_raw()
        elif not note_ids:
            print("Note ids are empty []")
        else:
            if raw:
                all_notes = [self.get_note_raw(note_id) for note_id in note_ids]
            else:
                all_notes = [self.get_note(note_id) for note_id in note_ids]
            print("All notes retrieved: ", all_notes)
        return all_notes


    # UPDATE METHODS
    def update_note(self, note_id, title, content):
        note_ref = self.ref_notes.child(str(note_id))
        note_ref.update({"title": title, "content": content})

        
    def delete_note_raw(self, id):
        self.ref_notes.child(str(id)).delete()
        
    def delete_note_from_user(self, user_id, note_id):
        user = self.get_user(user_id)
        if note_id in user.notes:
            user.notes.remove(note_id)
            self.ref_users.child(str(user_id)).update({"notes": user.notes})

    def delete_note(self, note_id):
        # İlk olarak notu tüm kullanıcılardan sil
        note = self.get_note_raw(note_id)
        if note is not None:
            user_ids = note.get('user_ids', [])
            for user_id in user_ids:
                self.delete_note_from_user(user_id, note_id)
        # Daha sonra notu tamamen sil
        self.delete_note_raw(note_id)


# # # # # # # # # # # # #
#         USERS

    # ADD METHODS         
    def add_user(self, user_dictionary):
        self.add_user(user_dictionary["email"], user_dictionary["password"], user_dictionary["name"], user_dictionary["notes"])

    def add_user(self, email, password, name, notes):
        user_id = self.get_last_id("user")+1
        user = User(user_id, email, password, name, notes)
        self.ref_users.child(str(user_id)).set(user.__dict__)

    # GET METHODS
    def get_users_raw(self):
        return self.ref_users.get()

    def get_user_raw(self, uid):
        a = self.ref_users.order_by_key().equal_to(str(uid)).limit_to_first(1).get()
        a.pop(0) if a[0] is None else ""
        return a[0]


    def get_user(self, uid):
        raw_user = self.get_user_raw(uid)
        user = self.make_obj(raw_user, "user")
        return user
    
    def get_emails(self):
        emails = []
        users = self.ref_users.get()
        for user in users:
            if user is not None:
                emails.append(user["email"])
        return emails
    
    def is_user_exists(self, email, pw, get_user=False, get_user_obj=False):
        for u in self.get_users_raw():
            if email == u["email"] and pw == u["password"]:
                if get_user_obj: 
                    return self.make_obj(u, "user") # we wanna get the user as an <User> object
                elif get_user:
                    return u # we wanna get the user but in a dictionary form (RAW)
                else:
                    return True # if we only wanna know that user is exist or not.
        return False # if user cannot be found.

    def get_uid(self, search, _type="name"):
        for u in self.get_users_raw():
            if search == u[_type]:
                return u["id"]