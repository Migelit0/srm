import datetime
import sqlalchemy
from sqlalchemy import orm, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    students = Column(String, nullable=False)  # split ;;
    teacher_id = Column(Integer, nullable=True)
    # teacher = orm.relation('Users')
    lessons = orm.relation('Lessons', back_populates='group')
