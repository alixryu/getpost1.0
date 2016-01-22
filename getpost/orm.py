""":mod:`getpost.orm` --- Object relational mapper module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use thread-local sessions to manage database sessions
Reference : http://docs.sqlalchemy.org/en/latest/orm/contextual.html
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from .config import DevConfig as config


class ReprBase(object):
    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(['%s=%r' % (key, getattr(self, key))
                       for key in sorted(self.__dict__.keys())
                       if not key.startswith('_')])
            )


Base = declarative_base(cls=ReprBase)

engine = create_engine(config.DB_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
