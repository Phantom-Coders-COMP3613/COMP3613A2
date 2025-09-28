from .user import User
from App.database import db

class Student(User):
    __tablename__ = 'student'
    studentId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    hours = db.Column(db.Float, default=0.0)

    accolades = db.relationship('Accolades', backref='student', uselist=False)
    confirmation = db.relationship('Confirmation', backref='student', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)

    def __repr__(self):
        return f'<Student {self.username} - Hours {self.hours}>'

class Staff(User):
    __tablename__ = 'staff'
    staffId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __init__(self, username, password):
        super().__init__(username, password)

    def __repr__(self):
        return f'<Staff {self.username}>'

# Represents pending hours volunteered, needed to be confirmed by staff
class Confirmation(db.Model):
    __tablename__ = 'confirmation'
    confirmationId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    hours = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Confirmation {self.confirmationId} with {self.hours} hours made by student {self.studentId}>'

# Represents accolades achieved by students
class Accolades(db.Model):
    __tablename__ = 'accolades'
    accoladeId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    milestone10 = db.Column(db.Boolean, default=False)
    milestone25 = db.Column(db.Boolean, default=False)
    milestone50 = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Accolades achieved by student {self.studentId}: 10 hours: {self.milestone10}, 25 hours: {self.milestone25}, 50 hours: {self.milestone50}>'
    
    
