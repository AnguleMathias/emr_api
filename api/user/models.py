from sqlalchemy import (Column, String, Integer,
                        ForeignKey, Table, Enum, Index)
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence

from helpers.database import Base
from utilities.utility import Utility, StateType
from utilities.validations import validate_empty_fields

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE")),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"))
)


class User(Base, Utility):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    state = Column(Enum(StateType), default="active")
    roles = relationship(
        'Role',
        secondary="users_roles",
        backref=('users_association'),
        lazy="joined")

    __table_args__ = (
        Index(
            'ix_unique_user_content',
            'name',
            unique=True,
            postgresql_where=(state == 'active')),
    )

    def __init__(self, **kwargs):
        validate_empty_fields(**kwargs)

        self.email = kwargs['email']
        self.name = kwargs['name']
        self.picture = kwargs['picture']
