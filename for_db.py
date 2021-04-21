from data import db_session
from data.attendance import Attendance
from data.groups import Group
from data.lessons import Lessons
from data.payment import Payment


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


def add_payment(lesson_id):
    db_session.global_init("db/main.db")
    db_sess = db_session.create_session()
    group_id = db_sess.query(Lessons.group_id).filter(Lessons.id == lesson_id).first()[0]
    group = db_sess.query(Group).filter(Group.id == group_id).first()
    student_ids = list(map(int, db_sess.query(Group.students).filter(Group.id == group_id).first()[0].split(';;')))

    all_lessons = list(map(lambda x: int(x[0]),
                           db_sess.query(Payment.lesson_number).filter(Payment.lesson_id == lesson_id).all()))
    if all_lessons:
        new_lesson_number = max(all_lessons) + 1
    else:
        new_lesson_number = 1

    for user_id in student_ids:
        new_payment = Payment(
            student_id=user_id,
            lesson_id=lesson_id,
            lesson_number=new_lesson_number,
            is_payed=False
        )
        db_sess.add(new_payment)
    db_sess.commit()

def make_it_correct(student_id):
    pass

if __name__ == '__main__':
    add_payment(2)
