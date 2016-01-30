""":mod:`tests.hogwarts.househead` --- Test module getpost.hogwarts.househead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from nose.tools import eq_, ok_

from flask import session as user_session
from flask.ext.login import current_user
from werkzeug.exceptions import Forbidden

from getpost.hogwarts.fatlady import authenticate_user
from getpost.hogwarts.househead import requires_roles
from getpost.hogwarts.househead import EMPLOYEE_ROLE, STUDENT_ROLE

from .. import app, driver


# TODO: automate creating the accounts below
# one-role account (student)
email_address1 = 'gsquirrel@oberlin.edu'
password1 = 'anywhere'

# two-role account (student, employee)
email_address2 = 'asquirrel@oberlin.edu'
password2 = 'tappansquare'

# role change alert messages
role_change_success_alert = '×\nRole has been successfully changed.'
role_change_failure_alert = '×\nRole could not be changed.'


def test_requires_roles():

    @requires_roles(EMPLOYEE_ROLE)
    def test_func():
        return True

    with app.test_request_context():
        # login with two-role account
        account = authenticate_user(email_address2, password2, False)
        ok_(account is not None)
        eq_(int(user_session['user_id']), account.id)
        eq_(user_session['email_address'], email_address2)
        # check that current role is employee
        eq_(user_session['current_role'], EMPLOYEE_ROLE)

        # tackle parcels.view_packages_by_student_id (employee only)
        ok_(test_func())

        # switch role to student
        current_user.switch_current_role(STUDENT_ROLE)
        # check that current role is student
        eq_(user_session['current_role'], STUDENT_ROLE)

        # tackle parcels.view_packages_by_student_id (employee only)
        try:
            test_func()
            ok_(False)
        except Forbidden:
            ok_(True)


def test_switch_role_selenium():
    # login with an account with one role
    driver.get('http://localhost:5000/auth/login/')
    driver.find_element_by_name('email').send_keys(email_address1)
    driver.find_element_by_name('password').send_keys(password1)
    driver.find_element_by_name('submit').click()
    ok_('Hello '+email_address1 in driver.page_source)
    ok_('Log Out' in driver.page_source)

    # fail in finding the role switch link
    ok_('Role' not in driver.page_source)

    # login with an account with two roles
    driver.get('http://localhost:5000/auth/login/')
    driver.find_element_by_name('email').send_keys(email_address2)
    driver.find_element_by_name('password').send_keys(password2)
    driver.find_element_by_name('submit').click()
    ok_('Hello '+email_address2 in driver.page_source)
    ok_('Log Out' in driver.page_source)

    # succeed in switching back and forth to other available role
    driver.find_element_by_link_text('Role').click()
    driver.find_element_by_link_text('Employee').click()
    message = driver.find_element_by_class_name('alert').text
    eq_(message, role_change_success_alert)

    driver.find_element_by_link_text('Role').click()
    driver.find_element_by_link_text('Student').click()
    message = driver.find_element_by_class_name('alert').text
    eq_(message, role_change_success_alert)

    # fail in switching to unavailable role
    driver.get('http://localhost:5000/role/admininstrator_role')
    message = driver.find_element_by_class_name('alert').text
    eq_(message, role_change_failure_alert)

    # logout
    driver.find_element_by_link_text('Log Out').click()
