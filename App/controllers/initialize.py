from .user import create_user, create_staff, create_student
from App.database import db
from .controllers import log_hours, request_confirmation


def initialize():
    db.drop_all()
    db.create_all()
    create_student('bob', 'bobpass')
    create_student('rob', 'robpass')
    create_student('alice', 'alicepass')
    
    create_staff('admin', 'adminpass')
    create_staff('staff1', 'staff1pass')
    create_staff('staff2', 'staff2pass')

    request_confirmation(1, 20.5)
    request_confirmation(2, 300.0)
    request_confirmation(1, 10.5)
    request_confirmation(3, 4.0)
    request_confirmation(2, 2.0)
    request_confirmation(1, 5.0)
    request_confirmation(3, 3.5)

    log_hours(1, "Y")
    log_hours(2, "Y")
    log_hours(3, "N")
    log_hours(4, "Y")