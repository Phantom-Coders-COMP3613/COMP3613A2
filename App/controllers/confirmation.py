from App.models import Student, Confirmation
from App.database import db
from .accolades import update_accolades

# (Staff) View all pending confirmations
def view_confirmations():
    confirmations = Confirmation.query.all()
    for confirmation in confirmations:
        print(confirmation)

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
