from data import db_session


def add_attendances(lesson_id):
    db_session.global_init("db/main.db")
    db_sess = db_session.create_session()
    
