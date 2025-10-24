import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff, User, Confirmation, Accolades, Student
from App.controllers import (
    create_staff,
    create_student,
    login,
    student_request_confirmation
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_staff(self):
        newstaff = Staff("staff1", "staff1pass", "S010")
        assert newstaff.username == "staff1"
        assert newstaff.staffId == "S010"
        assert newstaff.user_type == "staff"
        assert isinstance(newstaff, Staff)
        
    def test_new_student(self):
        newstudent = Student("student1", "studentpass")
        assert newstudent.username == "student1"
        
    def test_new_confirmation(self):
        newstudent = Student("student2", "student2pass")
        newconfirmation = Confirmation(studentId=newstudent.id, hours=50.0)
        assert newconfirmation.studentId == newstudent.id and newconfirmation.hours == 50.0
        
    def test_new_accolades(self):
        newstudent = Student("student3", "student3pass")
        newaccolades = Accolades(studentId=newstudent.id)
        assert newaccolades.studentId == newstudent.id
        
    # pure function no side effects or integrations called
    def test_staff_get_json(self):
        staff = Staff("staff1", "staff1pass", "S001")
        staff_json = staff.get_json()
        self.assertDictEqual(staff_json, {"id":staff.id, "username":"staff1", "staff_id":"S001", "user_type":"staff"})
        
    def test_student_get_json(self):
        student = Student("student1", "student1pass")
        student_json = student.get_json()
        self.assertDictEqual(student_json, {"id":student.id, "username":"student1", "user_type":"student"})

    def test_hashed_password(self):
        password = "student4pass"
        user = User("student4", password)
        assert user.password != password

    def test_check_password(self):
        password = "student4pass"
        user = User("student4", password)
        assert user.check_password(password)

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

class UsersIntegrationTests(unittest.TestCase):
    def test_student_request_confirmation():
        student = create_student("student1", "student1pass")
        request = student_request_confirmation(student.id, 10.0)
        assert request.studentId == 1
        assert request.hours == 10.0