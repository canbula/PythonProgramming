from db import Firebase


class Professor:
    def __init__(self, user_id: str, f: Firebase) -> None:
        self.user_id = user_id
        self.title = ""
        self.fullname = ""
        self.department = ""
        self.university = ""
        self.courses = []
        self.f = f
        self.ref = f.ref.child("professors").child(self.user_id)
        if self.ref.get():
            self.get()

    def save(self):
        self.ref.set(
            {
                "title": self.title,
                "fullname": self.fullname,
                "department": self.department,
                "university": self.university,
            }
        )
        return self

    def update(self, updates: dict = {}):
        if updates:
            self.title = updates.get("title", self.title)
            self.fullname = updates.get("fullname", self.fullname)
            self.department = updates.get("department", self.department)
            self.university = updates.get("university", self.university)
        self.save()
        return self

    def get(self):
        professor = self.ref.get()
        if not professor:
            return self
        self.title = professor["title"]
        self.fullname = professor["fullname"]
        self.department = professor["department"]
        self.university = professor["university"]
        courses = self.f.ref.child("courses").get()
        if courses:
            for course_id in courses:
                course = courses[course_id]
                if course["user_id"] == self.user_id:
                    self.courses.append(course)
        return self

    def delete(self):
        self.ref.delete()
        self.title = ""
        self.fullname = ""
        self.department = ""
        self.university = ""
        return self

    def __str__(self):
        return f"{self.title} {self.fullname} @ {self.department}, {self.university}"


if __name__ == "__main__":
    f = Firebase()
    f.login("prof@university.edu", "password")
    professor = Professor(f.get_user_id(), f)
    professor.title = "Assoc. Prof. Dr."
    professor.fullname = "Bora Canbula"
    professor.department = "Computer Engineering"
    professor.university = "Manisa Celal Bayar University"
    professor.save()
    print(professor)
    print(professor.courses)
    professor.update(
        {
            "title": "Prof. Dr.",
            "department": "Department of Computer Engineering",
        }
    )
    print(professor)
    professor.delete()
