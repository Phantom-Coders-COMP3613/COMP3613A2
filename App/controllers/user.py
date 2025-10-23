from App.models import User, Student, Staff
from App.database import db

def create_student(username, password):
    newstudent = Student(username=username, password=password)
    try:
        db.session.add(newstudent)
        db.session.commit()
        return newstudent
    except Exception as e:
        db.session.rollback()
        print(f"Error creating student: {e}")
        return None

def create_staff(username, password, staff_id):
    newstaff = Staff(username=username, password=password, staff_id=staff_id)
    try:
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    except Exception as e:
        db.session.rollback()
        print(f"Error creating staff: {e}")
        return None
