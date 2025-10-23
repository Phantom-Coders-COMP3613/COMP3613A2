from App.models import Student, Confirmation, Staff, User
from App.database import db

# (Staff) View all pending confirmations
def view_confirmations():
    confirmations = Confirmation.query.filter_by(status='pending').all()
    for confirmation in confirmations:
        print(confirmation)

# (Staff) Log confirmation for student
def staff_log_confirmation(staff_id, confirmation_id):
    confirmation = Confirmation.query.get(confirmation_id)
    staff = Staff.query.get(staff_id)
    student = Student.query.get(confirmation.studentId)
    if not confirmation or not staff or not student:
        return None

    if confirmation.status != 'pending':
        print(f'Confirmation {confirmation_id} is not pending.')
        return None

    staff.log_confirmation(student, confirmation)
    return confirmation

# (Staff) Deny confirmation for student
def staff_deny_confirmation(staff_id, confirmation_id):
    confirmation = Confirmation.query.get(confirmation_id)
    staff = Staff.query.get(staff_id)
    if not confirmation or not staff:
        return None

    staff.deny_confirmation(confirmation)
    return confirmation

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
