from sqlalchemy import orm, Integer, Boolean, String, Column
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    classes = orm.relation("Classes",
                          secondary="class_to_teacher_table",
                          backref="teachers")
