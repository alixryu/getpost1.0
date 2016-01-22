""":mod:`getpost.config` --- Configuration module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os
from os.path import expanduser

PASSWORD_FILE = '~/.pgpass'
DEFAULT_PORT = 5432
DATABASE_NAME = 'getpost1'
DEFAULT_DB_URI = 'postgresql+psycopg2://user:password@ip:port/db_name'


# Try to find a user/password/host list for the database in the user's
# ~/.pgpass file.
# Return the properly-formatted URI on the first appropriate line, or None if
# none are found.
def getdefaultURI():
    try:
        with open(expanduser(PASSWORD_FILE), 'r') as f:
            for line in f.read().splitlines():
                host, port, database, user, password = line.split(':')
                if database == DATABASE_NAME:
                    if port == '':
                        port = DEFAULT_PORT
                    result = 'postgresql://{}:{}@{}:{}/{}'.format(
                        user, password, host, port, database
                    )
                    del password  # Don't want to leave this lying around.
                    return result
    except FileNotFoundError:
        print('could not open {}: file not found'.format(PASSWORD_FILE))
    except PermissionError:
        print('could not open {}: permission denied'.format(PASSWORD_FILE))
    except IsADirectoryError:
        print('could not open {}: is a directory'.format(PASSWORD_FILE))
    except Exception as e:
        print('exception occured while trying to open/read {}: {}'.format(
            PASSWORD_FILE, e)
            )
    return None


class Config(object):
    DB_URI = getdefaultURI()
    if DB_URI is None:
        DB_URI = DEFAULT_DB_URI
    SECRET_KEY = 'DO NOT USE IN PRODUCTION'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_SUBJECT_PREFIX = '[GETPOST] '
    MAIL_SENDER = 'GetPost Mailroom <obie.getpost@gmail.com>'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'  # Taken from Flask docs


class TestConfig(Config):
    DEBUG = True
    TESTING = True
