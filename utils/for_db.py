from data import db_session
from data.attendance import Attendance
from data.lessons import Lessons
from data.groups import Group
from data.users import User


def add_attendances(lesson_id):
    db_session.global_init("db/main.db")
    db_sess = db_session.create_session()
