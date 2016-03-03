""":mod:`getpost.hogwarts.wizards` --- Student information controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask.ext.login import login_required, current_user as account
from sqlalchemy_searchable import search

from ..forms import ModelForm, StudentSearchForm
from ..models import Student
from ..orm import Session as db_session
from .househead import requires_roles, EMPLOYEE_ROLE, STUDENT_ROLE


wizards_blueprint = Blueprint('wizards', __name__, url_prefix='/students')


@wizards_blueprint.route('/')
@login_required
@requires_roles(EMPLOYEE_ROLE, STUDENT_ROLE)
def wizards_index():
    if account.get_current_role() == STUDENT_ROLE:
        return redirect(url_for('.view_student_self'), 303)
    else:
        return redirect(url_for('.search_students'), 303)


@wizards_blueprint.route('/me/')
@login_required
@requires_roles(STUDENT_ROLE)
def view_student_self():
    student = account.student.student
    StudentForm = ModelForm(
        Student,
        db_session,
        exclude=['packages', 'role', 'search_vector']
        )
    student_form = StudentForm(obj=student)
    return render_template('wizards.html', student_form=student_form)


@wizards_blueprint.route('/<int:student_id>/')
@login_required
@requires_roles(EMPLOYEE_ROLE)
def view_student_detail(student_id):
    student = db_session.query(
            Student
            ).filter_by(id=student_id).first()

    if not student:
        abort(404)

    StudentForm = ModelForm(
        Student,
        db_session,
        exclude=['packages', 'role']
        )
    student_form = StudentForm(obj=student)
    return render_template('wizards.html', student=student_form)


@wizards_blueprint.route('/all/')
@login_required
@requires_roles(EMPLOYEE_ROLE)
def view_students():
    students = db_session.query(
            Student
            ).all()

    if not students:
        abort(404)

    return render_template('wizards.html', students=students)


@wizards_blueprint.route('/<int:id>/', methods=['PUT'])
@login_required
@requires_roles(EMPLOYEE_ROLE)
def edit_student(id):
    # TODO: complete this function
    return render_template('wizards.html')


@wizards_blueprint.route('/results/')
@login_required
@requires_roles(EMPLOYEE_ROLE)
def search_students_result():
    search_query = request.args['query']
    students = search_model(Student, search_query)
    return render_template('wizards.html', students=students)


@wizards_blueprint.route('/search/', methods=['GET', 'POST'])
@login_required
@requires_roles(EMPLOYEE_ROLE)
def search_students():
    search_form = StudentSearchForm()

    if search_form.validate_on_submit():
        search_query = search_form.query.data
        return redirect(url_for('.search_students_result', query=search_query))
    return render_template('wizards.html', search_form=search_form)


def search_model(model, search_query):
    # TODO: move to hogwarts.accio.py
    base_query = db_session.query(model)

    query_strings = search_query.split()
    search_query = ' or '.join(query_strings)

    search_result = search(base_query, search_query, sort=True)
    return search_result
