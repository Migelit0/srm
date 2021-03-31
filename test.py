from data import db_session
from data import attendance, lessons, users
from data.users import User
from data.lessons import Lessons
from data.attendance import Attendance

db_session.global_init("db/main.db")
db_sess = db_session.create_session()

# new_user = User(
#     name='test_name',
#     surname='test_surname',
#     type=1
# )
# new_user.set_password('test')
#
# db_sess.add(new_user)
# db_sess.commit()

# new_lesson = Lessons(
#     teacher_id=1,
#     date='1-18:00',
#     title='Math'
# )
# db_sess.add(new_lesson)
# db_sess.commit()

users_data = db_sess.query(User).first()
print(users_data)
