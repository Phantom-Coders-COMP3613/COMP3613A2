from App.models import Student, Accolades
from App.database import db

# (Student) View accolades (10/25/50 hours milestones)
def student_view_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        return None # Explicitly return None if student not found
    accolades = Accolades.query.filter_by(studentId=student_id).first()
    if not accolades:
        accolades = Accolades(studentId=student.id)
        db.session.add(accolades)
    return student.view_accolades(accolades)