# Flask Commands
$ flask init
# Initalizes dummy Student, Staff, Confirmation, and Accolade Objects in the database to test the various commands.

'''
STUDENT
'''
$ flask student create [username: String] [password: String]
# (EXTRA) Creates a Student with a Username and Password. (EXTRA)

$ flask student request_confirmation [student_id: int] [hours: float]
# (REQUIRED) Creates a Confirmation with hours attached and links it to the associated student_id.

$ flask student view_accolades [student_id: int]
# (REQUIRED) Shows the current milestone achieved by Student student_id, with the milestones being at 10/25/50 hours.

$ flask student view_leaderboard
# (REQUIRED) Shows a list of the students with the most hours, descending to the one with the least.

'''
STAFF
'''
$ flask staff create [username: String] [password: String]
# (EXTRA) Creates a Staff with a Username and Password.

$ flask staff log_hours [confirmation_id: int] [Y/N]
# (REQUIRED) If status="Y", queries the Confirmation confirmation_id, extracts its information and apply the hours worked to the relevant Student.
# If status="N", Confirmation will be denied, deleted, and command will be exited out of.

$ flask staff view_confirmations
# (EXTRA) Shows a list of all pending Confirmations.

$ flask staff view_leaderboard
# (REQUIRED) Shows a list of the students with the most hours, descending to the one with the least.
