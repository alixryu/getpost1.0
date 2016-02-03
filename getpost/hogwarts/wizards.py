""":mod:`getpost.hogwarts.wizards` --- Student information controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user as account

from ..forms import ModelForm
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
        return render_template('wizards.html')


@wizards_blueprint.route('/me/')
@login_required
@requires_roles(STUDENT_ROLE)
def view_student_self():
    student = account.student.student
    StudentForm = ModelForm(
        Student,
        db_session,
        exclude=['packages', 'role']
        )
    student_form = StudentForm(obj=student)
    return render_template('wizards.html', student=student_form)


@wizards_blueprint.route('/<int:student_id>/')
@login_required
@requires_roles(EMPLOYEE_ROLE)
def view_students(student_id):
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


@wizards_blueprint.route('/<int:id>/', methods=['PUT'])
@login_required
@requires_roles(EMPLOYEE_ROLE)
def edit_student(id):
    # TODO: complete this function
    return render_template('wizards.html')


@wizards_blueprint.route('/results/')
@login_required
@requires_roles(EMPLOYEE_ROLE)
def search_students():
    # TODO: complete this function
    return render_template('wizards.html')
