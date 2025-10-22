from App.models import User, Student, Staff
from App.database import db

def create_student(username, password):
    newstudent = Student(username=username, password=password)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def create_staff(username, password):
    newstaff = Staff(username=username, password=password)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def view_students():
    students = Student.query.all()
    for student in students:
        print(student)

def view_staff():
    staffs = Staff.query.all()
    for staff in staffs:
        print(staff)

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

# View Student Leaderboard
def view_leaderboard():
    students = Student.query.all()
    students.sort(key=lambda s: s.hours, reverse=True)
    for student in students:
        print(student)
