from App.models import Student, Accolades
from App.database import db

# Update accolades
def update_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        print(f'Student {student_id} not found.')
        return

    accolades = Accolades.query.filter_by(studentId=student.id).first()
    if not accolades:
        accolades = Accolades(studentId=student.id)
        db.session.add(accolades)

    if student.hours >= 50 and not accolades.milestone50:
        accolades.milestone50 = True
    if student.hours >= 25 and not accolades.milestone25:
        accolades.milestone25 = True
    if student.hours >= 10 and not accolades.milestone10:
        accolades.milestone10 = True

    db.session.commit()
    return None

# (Student) View accolades (10/25/50 hours milestones)
def view_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        return None # Explicitly return None if student not found
    update_accolades(student.id)
    return Accolades.query.filter_by(studentId=student_id).first()

