from data import db_session
from data import attendance, lessons, users
from data.users import User
from data.lessons import Lessons
from data.attendance import Attendance
from data.groups import Group
from datetime import datetime

db_session.global_init('db/main.db')
db_sess = db_session.create_session()
new_lesson = Lessons(
    teacher_id=1,
    date='6-18:00',
    title='Math',
    group_id=1
)
db_sess.add(new_lesson)
db_sess.commit()