from data import db_session
from data.attendance import Attendance
from data.lessons import Lessons
from data.groups import Group
from data.users import User


def add_attendances(lesson_id):
    db_session.global_init("db/main.db")
    db_sess = db_session.create_session()

    group_id = db_sess.query(Lessons.group_id).filter(Lessons.id == lesson_id).first()[0]

    student_ids = list(map(int, db_sess.query(Group.students).filter(Group.id == group_id).first()[0].split(';;')))
    # print(student_ids)
    all_lessons = list(map(lambda x: int(x[0]),
                           db_sess.query(Attendance.lesson_number).filter(Attendance.lesson_id == lesson_id).all()))
    if all_lessons:
        new_lesson_number = max(all_lessons) + 1
    else:
        new_lesson_number = 1

    for user_id in student_ids:
        new_attendance = Attendance(
            student_id=user_id,
            lesson_id=lesson_id,
            lesson_number=new_lesson_number,
            group_id=group_id
        )
        db_sess.add(new_attendance)

    db_sess.commit()


if __name__ == '__main__':
    add_attendances(2)
