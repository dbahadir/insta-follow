from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, BigInteger, SmallInteger
import datetime

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))

class InstaUser(Base):
    __tablename__ = 'insta_user';
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=0)
    insta_id = Column(BigInteger, nullable=False)
    user_name = Column(String(256))
    full_name = Column(String(512))
    is_private = Column(Boolean())
    is_related = Column(Boolean(), default=False)
    status = Column(SmallInteger, default=0)
    following_status = Column(SmallInteger, default=0)
    follower_status = Column(SmallInteger, default=0)
    following_date = Column(DateTime())
    unfollowing_date = Column(DateTime())
    follower_date = Column(DateTime())
    unfollower_date = Column(DateTime())
    created = Column(DateTime(), default=datetime.datetime.now)
