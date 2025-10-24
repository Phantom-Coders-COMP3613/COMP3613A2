import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_staff, create_student, initialize, request_confirmation, view_leaderboard, view_accolades, staff_log_confirmation, view_confirmations )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    db.session.commit()
    print('database intialized')

'''
Student Commands
'''

student_cli = AppGroup('student', help='Student object commands')

# (Extra) Create a student
@student_cli.command("create", help="Creates a student")
@click.argument("username", default="student")
@click.argument("password", default="studentpass")
def create_student_command(username, password):
    create_student(username, password)
    print(f"Student {username} created.")

# (Student) Request confirmation of hours (by staff)
@student_cli.command("request_confirmation", help="Request confirmation of hours (by staff)")
@click.argument("student_id")
@click.argument("hours")
def request_confirmation_command(student_id, hours):
    request_confirmation(student_id, hours)

# (Student) View accolades (10/25/50 hours milestones)
@student_cli.command("view_accolades", help="View accolades (10/25/50 hours milestones)")
@click.argument("student_id")
def view_accolades_command(student_id):
    accolade = view_accolades(student_id)
    if accolade.milestone50:
        print("Milestone 50 hours achieved!")
    elif accolade.milestone25:
        print("Milestone 25 hours achieved!")
    elif accolade.milestone10:
        print("Milestone 10 hours achieved!")
    else:
        print("No milestones achieved yet.")

# View Student Leaderboard
@student_cli.command("view_leaderboard", help="View Student Leaderboard")
def view_leaderboard_command():
    leaderboard = view_leaderboard()
    print("Student Leaderboard:")
    for student in leaderboard:
        print(f"{student.username}: {student.hours} hours")

app.cli.add_command(student_cli)

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

# (Extra) Create a staff
@staff_cli.command("create", help="Creates a staff")
@click.argument("username", default="admin")
@click.argument("password", default="adminpass")
def create_staff_command(username, password):
    create_staff(username, password)
    print(f"Staff {username} created.")

# (Staff) Log confirmation for student
@staff_cli.command("log_confirmation", help="Log confirmation for student")
@click.argument("staff_id")
@click.argument("confirmation_id")
def log_confirmation_command(staff_id, confirmation_id):
    staff_log_confirmation(staff_id, confirmation_id)

# (Extra) View all pending confirmations
@staff_cli.command("view_confirmations", help="View all pending confirmations")
def view_confirmations_command():
    view_confirmations()

# View Student Leaderboard
@staff_cli.command("view_leaderboard", help="View Student Leaderboard")
def view_leaderboard_command():
    view_leaderboard()

app.cli.add_command(staff_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)