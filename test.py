from data import db_session
from data import attendance, lessons, users
from data.users import User
from data.lessons import Lessons
from data.attendance import Attendance
from data.groups import Group

db_session.global_init("db/main.db")
db_sess = db_session.create_session()

new_user = User(
    name='teacher_name',
    surname='teacher_surname',
    type=1,
    login='teacher_login'
)
new_user.set_password('test')
db_sess.add(new_user)
new_user = User(
    name='student_name',
    surname='student_surname',
    type=2,
    login='login1'
)
new_user.set_password('test')
db_sess.add(new_user)

new_user = User(
    name='student_name2',
    surname='student_surname2',
    type=2,
    login='login2'
)
new_user.set_password('test')
db_sess.add(new_user)
db_sess.commit()

new_lesson = Lessons(
    teacher_id=1,
    date='1-18:00',
    title='Math',
    group_id=1
)
db_sess.add(new_lesson)
db_sess.commit()

new_lesson = Lessons(
    teacher_id=1,
    date='2-18:00',
    title='Math',
    group_id=1
)
db_sess.add(new_lesson)
db_sess.commit()

new_group = Group(
    students='3;;4',
    teacher_id=1
)
db_sess.add(new_group)

new_group = Group(
    students='3;;2',
    teacher_id=1
)
db_sess.add(new_group)
db_sess.commit()

new_lesson = Lessons(
    teacher_id=1,
    date='2-18:00',
    title='Title'
)
db_sess.add(new_lesson)
db_sess.commit()
