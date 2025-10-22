from App.models import Student
from App.database import db

# View Student Leaderboard
def view_leaderboard():
    students = Student.query.all()
    students.sort(key=lambda s: s.hours, reverse=True)
    for student in students:
        print(student)
    return students