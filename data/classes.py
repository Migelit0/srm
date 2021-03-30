from sqlalchemy import orm, Integer, Boolean, String, Column, Table, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class_to_teacher_table = Table(
    'association',
    SqlAlchemyBase.metadata,
    Column('teacher', Integer,
           ForeignKey('teacher.id')),
    Column('classes', Integer,
           ForeignKey('classes.id'))
)


class Classes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    title = Column(String, nullable=False)
