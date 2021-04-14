import datetime
import sqlalchemy
from sqlalchemy import orm, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Payment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student = orm.relation('User')
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    lesson = orm.relation('Lessons')
    lesson_number = Column(Integer, nullable=False)
    is_payed = Column(Boolean, default=False)