from .user import create_staff, create_student
from App.database import db
from .confirmation import staff_log_confirmation, staff_deny_confirmation, request_confirmation


def initialize():
    db.drop_all()
    db.create_all()
    create_student('bob', 'bobpass')
    create_student('rob', 'robpass')
    create_student('alice', 'alicepass')

    create_staff('admin', 'adminpass', 'SF1')
    create_staff('staff1', 'staff1pass', 'SF2')
    create_staff('staff2', 'staff2pass', 'SF3')

    request_confirmation(1, 20.5)
    request_confirmation(2, 300.0)
    request_confirmation(1, 10.5)
    request_confirmation(3, 4.0)
    request_confirmation(2, 2.0)
    request_confirmation(1, 5.0)
    request_confirmation(3, 3.5)

    staff_log_confirmation(4, 1)
    staff_log_confirmation(5, 2)
    staff_deny_confirmation(6, 3)
    staff_log_confirmation(4, 4)