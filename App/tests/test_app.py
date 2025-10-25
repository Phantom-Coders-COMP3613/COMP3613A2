from flask import request
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff, User, Confirmation, Accolades, Student
from App.controllers import (
    create_staff,
    create_student,
    login,
    student_request_confirmation,
    staff_log_confirmation,
    view_accolades,
    view_leaderboard
)

from App.controllers.leaderboard import view_leaderboard

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
        assert newconfirmation.studentId == newstudent.id 
        assert newconfirmation.hours == 50.0
        
    def test_new_accolades(self):
        newstudent = Student("student3", "student3pass")
        newaccolades = Accolades(studentId=newstudent.id)
        assert newaccolades.studentId == newstudent.id
        assert newaccolades.milestone10 == None
        assert newaccolades.milestone25 == None
        assert newaccolades.milestone50 == None
        
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

    def test_view_leaderboard_returns_list(self):
        # Create fake students in memory 
        class Student:
            def __init__(self, username, hours):
                self.username = username
                self.hours = hours
        students = [
            Student("alice", 10.0),
            Student("bob", 20.0),
            Student("charlie", 15.0)
        ]
        results = view_leaderboard(students)  # Pass fake data
        print(results)
        expected = [
            {"username": "bob", "hours": 20.0},
            {"username": "charlie", "hours": 15.0},
            {"username": "alice", "hours": 10.0}
        ]
       
        self.assertEqual(results, expected)
        self.assertIsInstance(results, list)  # Extra check for return type
    
    

    

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        create_db()
        yield app.test_client()
        db.drop_all()

#class UsersIntegrationTests(unittest.TestCase):


class TestLeaderboardIntegrationTests:
     
    def test_view_leaderboard_empty(self,empty_db): 
            results = view_leaderboard()
            assert results == [] #assuming db is empty

    
    def test_view_leaderboard_with_data(self):
        
    # Add test students to the database
            student1 = create_student("alice", "pass1")
            student1.hours = 10
            student2 = create_student("bob", "pass2")
            student2.hours = 20
            student3 = create_student("charlie", "pass3")
            student3.hours = 15
            db.session.commit()

            results = view_leaderboard()
            expected = [
            {"username": "bob", "hours": 20},
            {"username": "charlie", "hours": 15},
            {"username": "alice", "hours": 10}
            ]
            assert results == expected
class UserIntegrationTests(unittest.TestCase):
    def test_student_request_confirmation(empty_db): 
        """Ensures a confirmation object is created with correct 'pending' status."""
        
        student = create_student("teststudent", "testpass")
        
        hours = 10.0
        student_id = student.id
        request = student_request_confirmation(student_id, hours)
        assert isinstance(request, Confirmation)
        assert request.status == "pending"
        assert request.hours == hours
        assert request.studentId == student_id

    def test_staff_log_confirmation(empty_db):
        """TEST: Ensures staff can log a student's confirmation and update hours."""
        
        student = create_student("teststudent2", "testpass2") 
        staff = create_staff("teststaff", "staffpass", "S000")
        
        confirmation = student_request_confirmation(student.id, 15.0)
        logged_confirmation = staff_log_confirmation(staff.id, confirmation.confirmationId)
        updated_student = Student.query.get(student.id)
        
        assert isinstance(logged_confirmation, Confirmation)
        assert logged_confirmation.status == "logged"
        assert updated_student.hours == 15.0

    def test_milestone_10_award(empty_db):
        """TEST: Ensures the 10-hour milestone is awarded after logging 12 hours."""
        
        student = create_student("Jane_10", "janepass") 
        staff = create_staff("Staff_10", "staffpass", "S001")
        db.session.add_all([student, staff])
        db.session.commit()
        
        confirmation = student_request_confirmation(student.id, 12.0)
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
        
        confirmation = student_request_confirmation(student.id, 25.0)
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
        
        confirmation = student_request_confirmation(student.id, 50.0)
        db.session.commit()
        
        staff_log_confirmation(staff.id, confirmation.confirmationId)

        accolades_data = view_accolades(student.id)
        assert accolades_data.milestone10 == True
        assert accolades_data.milestone25 == True
        assert accolades_data.milestone50 == True
