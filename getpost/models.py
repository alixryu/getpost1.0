""":mod:`getpost.models` --- Model module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy import String, Boolean, Binary
from sqlalchemy.orm import relationship

from bcrypt import hashpw, gensalt
from flask import session as user_session
from flask.ext.login import UserMixin

from . import login_manager
from .orm import Base, Session


class Package(Base):
    __tablename__ = 'package'

    id = Column(Integer, primary_key=True)
    sender_name = Column(String)
    student_id = Column(Integer, ForeignKey('student.id'))
    arrival_date = Column(DateTime)
    pickup_date = Column(DateTime)
    received_by = Column(Integer, ForeignKey('employee_role.id'))
    status = Column(
        Enum('picked_up', 'not_picked_up', name='package_status_type')
        )
    is_deleted = Column(Boolean, default=False)
    last_edit_date = Column(DateTime)

    student = relationship(
        'Student',
        lazy='joined'
        )
    employee = relationship(
        'EmployeeRole',
        lazy='joined'
        )
    notifications = relationship('Notification')


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    email_address = Column(String)
    send_date = Column(DateTime)
    send_count = Column(Integer)

    package = relationship('Package')


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    alternative_name = Column(String)
    ocmr = Column(String)
    t_number = Column(String)
    email_address = Column(String)

    packages = relationship(
        'Package',
        lazy='joined'
        )
    role = relationship('StudentRole', uselist=False)


class Account(UserMixin, Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, unique=True)
    password = Column(Binary)
    verified = Column(Boolean)
    role = Column(
        Enum('student', 'employee', 'administrator', name='account_type')
        )

    student = relationship('StudentRole', uselist=False)
    employee = relationship('EmployeeRole', uselist=False)
    administrator = relationship('AdministratorRole', uselist=False)

    def set_password(self, password):
        self.password = hashpw(bytes(password, 'ASCII'), gensalt())

    def check_password(self, password):
        return self.password == hashpw(bytes(password, 'ASCII'), self.password)

    @login_manager.user_loader
    def load_account(account_id):
        db_session = Session()
        return db_session.query(Account).filter_by(id=int(account_id)).first()

    def log_in(self):
        user_session.update(
            {
                'email_address': self.email_address,
                }
            )

    def log_out(self):
        user_session.pop('email_address', None)


class AdministratorRole(Base):
    __tablename__ = 'administrator_role'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account')

    login_attributes = ['first_name', 'last_name']


class EmployeeRole(Base):
    __tablename__ = 'employee_role'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account')
    packages = relationship(
        'Package',
        lazy='joined'
        )

    login_attributes = ['first_name', 'last_name']


class StudentRole(Base):
    __tablename__ = 'student_role'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    first_name = Column(String)
    last_name = Column(String)
    student_info = Column(Integer, ForeignKey('student.id'))

    account = relationship('Account')
    student = relationship('Student')

    login_attributes = ['first_name', 'last_name']
