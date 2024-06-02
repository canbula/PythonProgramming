from db import Firebase
from professor import Professor


class Course:
    def __init__(self, user_id: str, f: Firebase) -> None:
        self.course_id = ""
        self.user_id = user_id
        self.title = ""
        self.description = ""
        self.ref = f.ref.child("courses")
        self.professor = Professor(user_id, f)

    def create(self):
        self.course_id = self.ref.push(
            {
                "title": self.title,
                "description": self.description,
                "user_id": self.user_id,
            }
        ).key
        return self

    def save(self):
        self.ref.child(self.course_id).set(
            {
                "title": self.title,
                "description": self.description,
                "user_id": self.user_id,
            }
        )
        return self

    def update(self, updates: dict = {}):
        if updates:
            self.title = updates.get("title", self.title)
            self.description = updates.get("description", self.description)
            self.user_id = updates.get("user_id", self.user_id)
        self.save()
        return self

    def get(self):
        course = self.ref.child(self.course_id).get()
        if not course:
            return self
        self.title = course["title"]
        self.description = course["description"]
        self.user_id = course["user_id"]
        return self

    def delete(self):
        self.ref.child(self.course_id).delete()
        self.title = ""
        self.description = ""
        self.user_id = ""
        return self

    def __str__(self):
        return f"{self.title} - {self.description} by {self.professor.title} {self.professor.fullname}"


if __name__ == "__main__":
    f = Firebase()
    f.login("prof@university.edu", "password")
    course = Course(f.get_user_id(), f)
    course.title = "Python Programming"
    course.description = (
        "Basic Concepts of Python Programming for Undergraduate Students"
    )
    course.create()
    print(course.course_id)
    print(course)
    course.title = "Advanced Python Programming"
    course.update()
    print(course)
    course.delete()
    print(course)
