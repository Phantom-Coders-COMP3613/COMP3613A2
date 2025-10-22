from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

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

