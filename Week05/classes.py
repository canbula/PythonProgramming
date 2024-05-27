class ClassName:
    """This is my first class."""
    pass


class Student:
    def __init__(
            self, 
            student_id: str,
            name: str,
            age: int
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age
        self.courses = []  # self.courses = list()
    
    def register(self, course):
        if course not in self.courses:
            self.courses.append(course)
    
    def drop(self, course):
        if course in self.courses:
            self.courses.remove(course)
    
    def __str__(self):
        return f"We have a student with the following information: {self.student_id}, {self.name}, {self.age}"
    
    def __repr__(self):
        return f"Student(\"7\", \"Bora Canbula\", 39)"


if __name__ == "__main__":
    object_name = ClassName()
    print(object_name)
    print(hex(id(object_name)))
    print(dir(object_name))
    print(object_name.__doc__)
    # print(help(object_name))
    print(object_name.__class__)
    print(object_name.__class__.__name__)
    print(object_name.__class__.__bases__)
    print(object_name.__class__.__module__)

    print(isinstance(object_name, ClassName))
    print(isinstance(object_name, int))
    print(isinstance(object_name, object))

    print(issubclass(ClassName, object))

    """
    a = 5
    print(isinstance(a, int))
    print(isinstance(a, object))
    """

    student = Student("7", "Bora Canbula", 39)
    print(student.student_id)
    print(student.name)
    print(student.age)
    print(student.courses)
    student.register("CSE 3244")
    print(student.courses)
    student.register("CSE 3237")
    print(student.courses)
    student.drop("CSE 3237")
    print(student.courses)
    print(student)
    print(student.__repr__())
    recreated_student = eval(repr(student))
    print(recreated_student)
