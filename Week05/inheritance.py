from classes import Student


faculty_members = [
    "Dr. Bora Canbula",
    "Dr. Feza Gursey",
    "Dr. Erdal Inonu",
    "Dr. Engin Arik"
]

required_keyword = [
    "machine learning",
    "deep learning"
]


class GraduateStudent(Student):
    def __init__(
            self, 
            student_id: str, 
            name: str, 
            age: int,
            advisor = None,
            thesis = None
    ) -> None:
        super().__init__(student_id, name, age)
        self.advisor = None
        self.thesis = None
        if advisor is not None:
            self.assign_advisor(advisor)
        if thesis is not None:
            self.propose_thesis(thesis)
    
    def assign_advisor(self, advisor):
        if advisor not in faculty_members:
            raise ValueError("The advisor is not a faculty member.")
        self.advisor = advisor
    
    def propose_thesis(self, thesis):
        if not any(keyword in thesis for keyword in required_keyword):
            raise ValueError("The thesis does not contain any of the required keywords.")
        self.thesis = thesis


if __name__ == "__main__":
    graduate_student = GraduateStudent("7", "Bora Canbula", 39)
    print(graduate_student.__class__.__bases__)
    print(isinstance(graduate_student, GraduateStudent))
    print(isinstance(graduate_student, Student))
    print(isinstance(graduate_student, object))
    graduate_student.register("CSE 3244")
    print(graduate_student.courses)
    print(graduate_student)
    advisor_choices = ["Dr. Nihat Berker", "Dr. Bora Canbula"]
    for advisor in advisor_choices:
        try:
            graduate_student.assign_advisor(advisor)
        except ValueError:
            print(f"{advisor} is not a faculty member. Trying the next one.")
        else:
            print(f"{advisor} is assigned as the advisor.")
            break
    thesis_choices = [
        "new trends in quantum physics",
        "deep learning in computer vision"
    ]
    for thesis in thesis_choices:
        try:
            graduate_student.propose_thesis(thesis)
        except ValueError:
            print(f"The thesis \"{thesis}\" does not contain any of the required keywords. Trying the next one.")
        else:
            print(f"The thesis \"{thesis}\" is proposed.")
            break
