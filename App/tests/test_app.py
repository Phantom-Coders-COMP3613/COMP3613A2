import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff, User, Student , Confirmation, Accolades
from App.controllers import (
    create_staff,
    create_student,
    login,
    request_confirmation,
    staff_log_confirmation,
    view_accolades,
    view_leaderboard
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = Staff("bob", "bobpass", "S001")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Staff("bob", "bobpass", "S001")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "staff_id":"S001"})

    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

    def test_new_accolades(self):
        """Ensures a new Accolade object initializes correctly with default values."""
        newaccolades = Accolades()
        assert newaccolades.milestone10 == None
        assert newaccolades.milestone25 == None
        assert newaccolades.milestone50 == None

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_student_request_confirmation(empty_db): 
    """Ensures a confirmation object is created with correct 'pending' status."""
    
    student = create_student("teststudent", "testpass") 
    db.session.add(student)
    db.session.commit()
    
    hours = 10.0
    student_id = student.id

    request = request_confirmation(student_id, hours)
    
    assert request is not None
    assert request.status == "pending"
    assert request.hours == hours
    assert request.studentId == student_id


def test_milestone_10_award(empty_db):
    """TEST: Ensures the 10-hour milestone is awarded after logging 12 hours."""
    
    student = create_student("Jane_10", "janepass") 
    staff = create_staff("Staff_10", "staffpass", "S001")
    db.session.add_all([student, staff])
    db.session.commit()
    
    confirmation = request_confirmation(student.id, 12.0)
    db.session.commit()
    
    staff_log_confirmation(staff.id, confirmation.confirmationId)

    accolades_data = view_accolades(student.id)
    assert accolades_data.milestone10 == True
    assert accolades_data.milestone25 == False
    assert accolades_data.milestone50 == False


def test_milestone_25_award(empty_db):
    """TEST: Ensures the 25-hour milestone is awarded after logging 25 hours."""
    
    student = create_student("Jane_25", "janepass") 
    staff = create_staff("Staff_25", "staffpass", "S002")
    db.session.add_all([student, staff])
    db.session.commit()
    
    confirmation = request_confirmation(student.id, 25.0)
    db.session.commit()
    
    staff_log_confirmation(staff.id, confirmation.confirmationId)

   
    accolades_data = view_accolades(student.id)
    assert accolades_data.milestone10 == True 
    assert accolades_data.milestone25 == True
    assert accolades_data.milestone50 == False


def test_milestone_50_award(empty_db):
    """TEST: Ensures the 50-hour milestone is awarded after logging 50 hours."""
    
    student = create_student("Jane_50", "janepass") 
    staff = create_staff("Staff_50", "staffpass", "S003")
    db.session.add_all([student, staff])
    db.session.commit()
    
    confirmation = request_confirmation(student.id, 50.0)
    db.session.commit()
    
    staff_log_confirmation(staff.id, confirmation.confirmationId)

    accolades_data = view_accolades(student.id)
    assert accolades_data.milestone10 == True
    assert accolades_data.milestone25 == True
    assert accolades_data.milestone50 == True