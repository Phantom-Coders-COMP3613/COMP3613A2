from App.models import Student, Staff, Confirmation, Accolades
from App.database import db

# (Staff) Log confirmation for student
def log_confirmation(confirmation_id):
    confirmation = Confirmation.query.get(confirmation_id)
    if not confirmation:
        print(f'Confirmation {confirmation_id} not found.')
        return

    student = Student.query.get(confirmation.studentId)
    if not student:
        print(f'Student {confirmation.studentId} not found.')
        return

    student.hours += confirmation.hours
    print(f'Confirmation {confirmation.confirmationId} approved.')
    db.session.delete(confirmation)

    update_accolades(student.studentId)
    db.session.commit()
    print(f'Logged {confirmation.hours} hours for student {student.username}.')

# (Staff) Deny confirmation for student
def deny_confirmation(confirmation_id):
    confirmation = Confirmation.query.get(confirmation_id)
    if not confirmation:
        print(f'Confirmation {confirmation_id} not found.')
        return
    db.session.delete(confirmation)
    db.session.commit()
    print(f'Confirmation {confirmation.confirmationId} denied and removed.')

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

# (Student) Request confirmation of hours (by staff)
def request_confirmation(student_id, hours):
    student = Student.query.get(student_id)
    if not student:
        print(f'Student {student_id} not found.')
        return
    confirmation = Confirmation(studentId=student_id, hours=hours)
    db.session.add(confirmation)
    db.session.commit()
    print(f'Confirmation {confirmation.confirmationId} request for {hours} hours by student {student_id} created.')

# View Student Leaderboard
def view_leaderboard():
    students = Student.query.all()
    students.sort(key=lambda s: s.hours, reverse=True)
    for student in students:
        print(student)

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

'''
Extra
'''

# (Staff) View all pending confirmations
def view_confirmations():
    confirmations = Confirmation.query.all()
    for confirmation in confirmations:
        print(confirmation)