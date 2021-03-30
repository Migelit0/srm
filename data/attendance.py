import datetime
import sqlalchemy
from sqlalchemy import orm, Column, String, Integer, Boolean
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Attendance(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    student = orm.relation('User')
    teacher_id = Column(Integer, nullable=True)
    teacher = orm.relation('User')
    lesson_id = Column(Integer, nullable=False)
    lesson = orm.relation('Lesson')
    is_attended = Column(Boolean, nullable=True, default=False)
