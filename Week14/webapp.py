from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("home.html", name="Classroom Attendance Tracker")


@app.route("/attendance", methods=["GET", "POST"])
def attendance_page():
    if request.method == "POST":
        student_id = request.form["student_id"]
        attendance_code = request.form["attendance_code"]
        print(f"Student ID: {student_id}")
        print(f"Attendance Code: {attendance_code}")
    else:
        return render_template("error.html", message="Invalid request method")


if __name__ == "__main__":
    app.run(debug=True)
