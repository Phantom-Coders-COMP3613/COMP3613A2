from .user import User
from App.database import db

# Represents accolades achieved by students
class Accolades(db.Model):
    __tablename__ = 'accolades'
    accoladeId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    milestone10 = db.Column(db.Boolean, default=False)
    milestone25 = db.Column(db.Boolean, default=False)
    milestone50 = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Accolades achieved by student {self.studentId}: 10 hours: {self.milestone10}, 25 hours: {self.milestone25}, 50 hours: {self.milestone50}>'
    