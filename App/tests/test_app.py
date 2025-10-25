import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff, User
from App.controllers import (
    create_staff,
    create_student,
    login
)

from App.controllers.leaderboard import view_leaderboard

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