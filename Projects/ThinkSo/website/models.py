import datetime


class Note:
    def __init__(self, id, user_ids, title="", content=""):
        self.id = id
        self.title = title
        self.content = content
        self.user_ids = user_ids
        self.date = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

class User:
    def __init__(self, id, email, password, name, notes=[]):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.notes = notes