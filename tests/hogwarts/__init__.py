""":mod:`tests.hogwarts` --- Test module of getpost.hogwarts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from nose.tools import eq_

from getpost.hogwarts import update_model
from getpost.orm import Session
from getpost.models import Account

from .. import app, driver
from .fatlady import test_authentication_integration
from .househead import test_requires_roles, test_switch_role_selenium


def test_update_model():
    email_address = 'zzz@oberlin.edu'
    password = bytes('zzz', 'ascii')
    verified = True
    role = 'employee'

    try:
        db_session = Session()

        # create dummy account
        account = Account(
            email_address=email_address,
            password=password,
            verified=False,  # to update 1
            role='student'  # to update 2
            )
        db_session.add(account)
        db_session.commit()

        # update account
        update_model(
            Account,
            Account.email_address.name,
            email_address,
            **{
                Account.verified.name: verified,
                Account.role.name: role
                }
            )

        # query updated dummy account
        account = db_session.query(
            Account
            ).filter_by(email_address=email_address).first()

        # test
        eq_(email_address, account.email_address)
        eq_(password, account.password)
        eq_(verified, account.verified)
        eq_(role, account.role)

    finally:
        # delete dummy account
        db_session.delete(account)
        db_session.commit()


def test_index_selenium():
    driver.get('http://localhost:5000/')

    result = driver.find_element_by_class_name('mission').text
    mission = ("GetPost is a 21st-century take on the Oberlin mailroom. We "
               "aim to save both students and employees a significant amount "
               "of time and energy by allowing package information to be "
               "stored and viewed online. No longer will anyone have to walk "
               "all the way up to Wilder Hall in order to check on a package, "
               "just to learn that it hasn't arrived yet and that they'll be "
               "forced to repeat themselves the day after! In short, GetPost "
               "brings the mailroom directly to you."
               )

    eq_(
        result,
        mission,
        'Home page contents are incorrect.'
        )


def test_ping():
    test_app = app.test_client()
    rv = test_app.get('/ping')
    rv_string = rv.data.decode('utf-8')
    eq_(
        rv_string,
        'What the brangan.',
        'Ping response string not identical'
    )
