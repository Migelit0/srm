from data import db_session
from data import attendance, lessons, users
from data.users import User
from data.lessons import Lessons
from data.attendance import Attendance
from data.groups import Group

db_session.global_init("db/main.db")
db_sess = db_session.create_session()
print(db_sess.query(Lessons).first().group.teacher_id)