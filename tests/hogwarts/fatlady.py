""":mod:`tests.hogwarts.fatlady` --- Test module of getpost.hogwarts.fatlady
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from nose.tools import eq_, ok_

from flask import session as user_session

from getpost.hogwarts.fatlady import authenticate_user, deauthenticate_user
from getpost.hogwarts.fatlady import create_account
from getpost.models import Account, Student
from getpost.orm import Session

from .. import app, driver


email_address = 'asquirrel@oberlin.edu'
password = 'tappansquare'
remember_me = True
t_number = 'T01123456'

db_session = Session()


def test_authenticate_user():
    # test with non-existing account
    account = authenticate_user(
        'zzz@oberlin.edu', password, remember_me
        )
    ok_(account is None)
    ok_('user_id' not in user_session)
    ok_('email_address' not in user_session)

    # test with existing account, wrong password
    account = authenticate_user(email_address, 'zzzz', remember_me)
    ok_(account is None)
    ok_('user_id' not in user_session)
    ok_('email_address' not in user_session)

    # test with existing account, correct password
    account = authenticate_user(email_address, password, remember_me)
    ok_(account is not None)
    eq_(int(user_session['user_id']), account.id)
    eq_(user_session['email_address'], email_address)


def test_login_selenium():
    # TODO: test remember_me

    # test with non-existing account
    driver.get('http://localhost:5000/auth/login/')
    driver.find_element_by_name('email').send_keys('zzzz@oberlin.edu')
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('submit').click()
    ok_('Hello '+email_address not in driver.page_source)
    ok_('Log Out' not in driver.page_source)

    # test with existing account, wrong password
    driver.get('http://localhost:5000/auth/login/')
    driver.find_element_by_name('email').send_keys(email_address)
    driver.find_element_by_name('password').send_keys('zzzz')
    driver.find_element_by_name('submit').click()
    ok_('Hello '+email_address not in driver.page_source)
    ok_('Log Out' not in driver.page_source)

    # test with existing account, correct password
    driver.get('http://localhost:5000/auth/login/')
    driver.find_element_by_name('email').send_keys(email_address)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('submit').click()
    ok_('Hello '+email_address in driver.page_source)
    ok_('Log Out' in driver.page_source)


def test_deauthenticate_user():
    deauthenticate_user()
    ok_('user_id' not in user_session)
    ok_('email_address' not in user_session)


def test_logout_selenium():
    driver.find_element_by_link_text('Log Out').click()
    ok_('Hello '+email_address not in driver.page_source)
    ok_('Log Out' not in driver.page_source)
    eq_(driver.current_url, 'http://localhost:5000/')


def test_create_account():
    # test with a new, match account
    eq_(create_account(email_address, t_number, password), 1)
    # test existence of new Account, StudentRole object
    account = db_session.query(
        Account
        ).filter_by(email_address=email_address).first()
    ok_(account)
    ok_(account.student)
    ok_(account.student.student)

    # test with already existing account
    eq_(create_account(email_address, t_number, password), -1)

    # test with no match account
    eq_(create_account('zzzz@oberlin.edu', t_number, password), 0)

    # remove account
    db_session.delete(account)
    db_session.commit()
    account = db_session.query(
        Account
        ).filter_by(email_address=email_address).first()
    ok_(account is None)


def test_signup_selenium():
    # test correct values
    driver.get('http://localhost:5000/auth/signup/student/')
    driver.find_element_by_name('email').send_keys(email_address)
    driver.find_element_by_name('t_number').send_keys(t_number)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('password2').send_keys(password)
    driver.find_element_by_name('submit').click()
    ok_('Login' in driver.title)

    # test with different password
    driver.get('http://localhost:5000/auth/signup/student/')
    driver.find_element_by_name('email').send_keys(email_address)
    driver.find_element_by_name('t_number').send_keys(t_number)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('password2').send_keys(password+'a')
    driver.find_element_by_name('submit').click()
    ok_('Signup' in driver.title)

    # test with existing account
    driver.get('http://localhost:5000/auth/signup/student/')
    driver.find_element_by_name('email').send_keys(email_address)
    driver.find_element_by_name('t_number').send_keys(t_number)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('password2').send_keys(password)
    driver.find_element_by_name('submit').click()
    ok_('Signup' in driver.title)

    # test with no match
    driver.get('http://localhost:5000/auth/signup/student/')
    driver.find_element_by_name('email').send_keys('zzzz@oberlin.edu')
    driver.find_element_by_name('t_number').send_keys(t_number)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('password2').send_keys(password+'a')
    driver.find_element_by_name('submit').click()
    ok_('Signup' in driver.title)


def test_authentication_integration():
    # create dummy student instance
    student = Student(
        first_name='Albino',
        last_name='Squirrel',
        ocmr='0000',
        t_number=t_number,
        email_address=email_address
        )
    db_session.add(student)
    db_session.commit()

    # sign up
    test_create_account()
    test_signup_selenium()

    # controller function tests
    with app.test_request_context():
        test_authenticate_user()
        test_deauthenticate_user()

    # selenium tests
    test_login_selenium()
    test_logout_selenium()

    # delete dummy account
    account = db_session.query(
        Account
        ).filter_by(email_address=email_address).first()
    db_session.delete(account)
    db_session.commit()

    # delete dummy student instance
    student = db_session.query(
        Student
        ).filter_by(email_address=email_address).first()
    db_session.delete(student)
    db_session.commit()
