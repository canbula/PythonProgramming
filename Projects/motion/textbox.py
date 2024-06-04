from db import Firebase
 
 
class TextBoxDb:
    def __init__(self, id: str, link:str, f: Firebase) -> None:
       
        self.class_ = "textbox"
        self.id = id
        self.paragraph = ""
        """
        self.ref = f.ref.child("textboxes")
        """
        self.textboxes = []  # Empty list to store TextBox objects
       
        self.f = f
       
        self.link = link
        self.ref = f.ref
        for i in link.split('/'):
            self.ref = self.ref.child(i)
 
    def create(self):
        self.ref.child(self.id).set(
            {
                "class_": self.class_,
                "id": self.id,
                "paragraph": self.paragraph,
            })
       
           
        self.textboxes.append(self)  # Add created textbox to the list
        return self
 
    
 
if __name__ == "__main__":
    f = Firebase()
    f.login("prof@university.edu", "password")
    textBox= TextBoxDb(1, "quick_note", f)
    textBox.class_ = "Python "
    textBox.id = (
        "Basic "
    )
   
    textBox.create()
    