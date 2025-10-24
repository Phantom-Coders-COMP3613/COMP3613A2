from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type,
    }
    
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
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    hours = db.Column(db.Float, default=0.0)

    accolades = db.relationship('Accolades', backref='student', uselist=False)
    confirmation = db.relationship('Confirmation', backref='student', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
    
    def __init__(self, username, password):
        super().__init__(username, password)

    def __repr__(self):
        return f'<Student {self.username} - Hours {self.hours}>'
    
    def get_json(self):
        json_data = super().get_json()
        json_data['user_type'] = 'student'
        return json_data
    
    def request_confirmation(self, confirmation):
        db.session.add(confirmation)
        db.session.commit()
        print(f'Confirmation {confirmation.confirmationId} has been logged.')
        return confirmation

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    staffId = db.Column(db.String(20), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }
    
    def __init__(self, username, password, staff_id):
        super().__init__(username, password)
        self.staffId = staff_id

    def __repr__(self):
        return f'<Staff {self.username}>'
    
    def get_json(self):
        json_data = super().get_json()
        json_data['staff_id'] = self.staffId
        json_data['user_type'] = 'staff'
        return json_data
    
    def log_confirmation(self, student, confirmation):
        student.hours += confirmation.hours
        confirmation.status = 'logged'
        print(f'Confirmation {confirmation.confirmationId} logged.')
        db.session.commit()

        print(f'Logged {confirmation.hours} hours for student {student.username}.')
