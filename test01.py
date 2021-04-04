from data import db_session
from data import attendance, lessons, users
from data.users import User
from data.lessons import Lessons
from data.attendance import Attendance
from data.groups import Group

db_session.global_init("db/main.db")
db_sess = db_session.create_session()
new_admin = User(
    name='admin',
    surname='admin',
    type=3,
    login='admin')
new_admin.set_password('admin')
db_sess.add(new_admin)
db_sess.commit()
