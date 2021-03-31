import datetime
import sqlalchemy
from sqlalchemy import orm, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Lessons(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    teacher = orm.relation('User')
    date = Column(String, nullable=True)
    title = Column(String, nullable=True)
