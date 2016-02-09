""":mod:`tests.hogwarts.wizards` --- Test module of getpost.hogwarts.wizards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from nose.tools import eq_, ok_

from getpost.hogwarts.wizards import search_model
from getpost.models import Student
from getpost.orm import Session as db_session
from .. import driver


def test_search_students_selenium():
    driver.get('http://localhost:5000/students/search/')
    driver.find_element_by_name('query').send_keys('0000')
    driver.find_element_by_name('submit').click()
    ok_('0000' in driver.page_source)


def test_search_students_result():
    model = Student
    query = '0000'
    student = search_model(model, query)
    eq_(query, student[0].ocmr)


def create_dummy_student():
    albino = Student(
        first_name='Albino',
        last_name='Squirrel',
        alternative_name='Albert',
        ocmr='0000',
        t_number='T00000000',
        email_address='asqurrel@oberlin.edu'
        )
    db_session.add(albino)
    db_session.commit()


def delete_dummy_student():
    student = db_session.query(Student).filter_by(ocmr='0000').first()
    db_session.delete(student)
    db_session.commit()


def test_search_students_integration():
    create_dummy_student()
    try:
        # TODO: authenticate first (role: employee)
        # test_search_students_selenium()
        test_search_students_result()
    finally:
        delete_dummy_student()
