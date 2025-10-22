from .user import User
from App.database import db

# Represents pending hours volunteered, needed to be confirmed by staff
class Confirmation(db.Model):
    __tablename__ = 'confirmation'
    confirmationId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    hours = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Confirmation {self.confirmationId} with {self.hours} hours made by student {self.studentId}>'
