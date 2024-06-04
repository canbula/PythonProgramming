#database.py

import firebase_admin
from firebase_admin import credentials, db, auth
import pyrebase

class Firebase:
    def __init__(self):
        # Initialize Firebase Admin SDK with credentials and database URL
        CREDENTIALS_FILE = "cred.json"
        DATABASE_URL = "https://sftproject-a6eeb-default-rtdb.europe-west1.firebasedatabase.app/"
        API_KEY = "AIzaSyBgENniVkNeOgctnOFAl7GZm68J0wkAJHI"
        PROJECT_ID = "SFTProject"
        self.cred = credentials.Certificate(CREDENTIALS_FILE)
        firebase_admin.initialize_app(self.cred, {"databaseURL": DATABASE_URL})

        # Reference to the root of the Firebase Realtime Database
        self.ref = db.reference("/")
        self.config = {
            "apiKey": API_KEY,
            "authDomain": f"{PROJECT_ID}.firebaseapp.com",
            "databaseURL": DATABASE_URL,
            "storageBucket": f"{PROJECT_ID}.appspot.com",
        }
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()

    def login(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        return user

    def register(self, email, password):
        user = self.auth.create_user_with_email_and_password(email, password)
        return user

    def get_current_user(self):
        return self.auth.current_user

    def get_user_id(self):
        return self.auth.current_user["localId"]

    def get_user_email(self):
        return self.auth.current_user["email"]



    def logout(self):
        self.auth.current_user = None

if __name__ == "__main__":
    # Instantiate Firebase object
    f = Firebase()

    # Access and modify data in Realtime Database
    print(f.ref.get())
    f.ref.set({"name": "Enis Bulut"})
    print(f.ref.get())

    try:
        # Try logging in with existing user credentials
        f.login("example@gmail.com", "password")
    except Exception as e:
        # If login fails, register a new user
        f.register("example@gmail.com", "password")

    # Get details of current authenticated user
    print(f.get_current_user())
