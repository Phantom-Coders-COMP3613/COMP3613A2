import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.controllers.user import create_staff, create_student
from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, request_confirmation, view_leaderboard, view_accolades, log_hours, view_confirmations, view_students )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Student Commands
'''

student_cli = AppGroup('student', help='Student object commands')

# (Extra) Create a student
@student_cli.command("create", help="Creates a student")
@click.argument("username", default="alice")
@click.argument("password", default="alicepass")
def create_student_command(username, password):
    create_student(username, password)

# (Student) Request confirmation of hours (by staff)
@student_cli.command("request_confirmation", help="Request confirmation of hours (by staff)")
@click.argument("student_id", default="1")
@click.argument("hours", default="2.5")
def request_confirmation_command(student_id, hours):
    request_confirmation(student_id, hours)


# View Student Leaderboard
@student_cli.command("view_leaderboard", help="View Student Leaderboard")
def view_leaderboard_command():
    view_leaderboard()


# (Student) View accolades (10/25/50 hours milestones)
@student_cli.command("view_accolades", help="View accolades (10/25/50 hours milestones)")
@click.argument("student_id", default="1")
def view_accolades_command(student_id):
    view_accolades(student_id)

app.cli.add_command(student_cli)

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

# Extra) Create a staff
@staff_cli.command("create", help="Creates a staff")
@click.argument("username", default="staff3")
@click.argument("password", default="staff3pass")
def create_staff_command(username, password):
    create_staff(username, password)

# (Staff) Log hours for student
@staff_cli.command("log_hours", help="Log hours for student")
@click.argument("confirmation_id", default="1")
def log_hours_command(confirmation_id):
    log_hours(confirmation_id)

# (Extra) View all pending confirmations
@staff_cli.command("view_confirmations", help="View all pending confirmations")
def view_confirmations_command():
    view_confirmations()

# (Extra) View all students
@staff_cli.command("view_students", help="View all students")
def view_students_command():
    view_students()

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