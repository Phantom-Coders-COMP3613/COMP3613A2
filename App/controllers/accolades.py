from App.models import Student, Accolades
from App.database import db

# Update accolades
def update_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        print(f'Student {student_id} not found.')
        return

    accolades = Accolades.query.filter_by(studentId=student.studentId).first()
    if not accolades:
        accolades = Accolades(studentId=student.studentId)
        db.session.add(accolades)

    if student.hours >= 50:
        accolades.milestone50 = True
    if student.hours >= 25:
        accolades.milestone25 = True
    if student.hours >= 10:
        accolades.milestone10 = True

    db.session.commit()
    print(f'Accolades for student {student.username} updated.')

# (Student) View accolades (10/25/50 hours milestones)
def view_accolades(student_id):
    accolade = Accolades.query.filter_by(studentId=student_id).first()
    if accolade.milestone50:
        print("Milestone 50 hours achieved!")
    elif accolade.milestone25:
        print("Milestone 25 hours achieved!")
    elif accolade.milestone10:
        print("Milestone 10 hours achieved!")
    else:
        print("No milestones achieved yet.")