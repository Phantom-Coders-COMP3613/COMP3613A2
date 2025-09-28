# Flask Commands

'''
STUDENT
'''
$ flask student create [username: String], [password: String]
# (EXTRA) Creates a Student with a Username and Password. (EXTRA)

$ flask student request_confirmation [student_id: int], [hours: float]
# (REQUIRED) Creates a Confirmation with hours attached and links it to the associated student_id.

$ flask student view_leaderboard
# (REQUIRED) Shows a list of the students with the most hours, descending to the one with the least.

$ flask student view_accolades [student_id: int]
# (REQUIRED) Shows the current milestone achieved by Student student_id, with the milestones being at 10/25/50 hours.

'''
STAFF
'''
$ flask staff create [username: String], [password: String]
# (EXTRA) Creates a Staff with a Username and Password.

$ flask staff log_hours [confirmation_id]
# (REQUIRED) Queries the Confirmation confirmation_id, extracts its information and apply the hours worked to the relevant Student.

$ flask staff view_confirmations
# (EXTRA) Shows a list of all pending Confirmations.

$ flask staff view_students
# (EXTRA) Shows a list of all students, even ones not on the leaderboard.
