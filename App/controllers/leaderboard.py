from App.models import Student
from App.database import db

# View Student Leaderboard
def view_leaderboard():
    return Student.query.all().sort(key=lambda s: s.hours, reverse=True)
