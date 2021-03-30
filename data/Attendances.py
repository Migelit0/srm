from sqlalchemy import orm, Integer, Boolean, String, Column
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    student = orm.relation('Student', )
    surname = Column(String, nullable=False)
    attendance = orm.relation('Attendance', back_populates='student')
