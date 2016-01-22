""":mod:`getpost.hogwarts.wizards` --- Student information controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Blueprint, render_template, redirect, url_for
from flask import abort, session as user_session
from flask.ext.login import login_required

from ..models import Account
from ..orm import Session

wizards_blueprint = Blueprint(
    'wizards',
    __name__,
    url_prefix='/students'
)


@wizards_blueprint.route('/')
@login_required
def wizards_index():
    db_session = Session()

    account = db_session.query(
        Account
        ).filter_by(id=user_session['user_id']).first()
    if account.student:
        return redirect(url_for('.view_student_self'), 303)
    else:
        return render_template('wizards.html')


@wizards_blueprint.route('/me/')
@login_required
def view_student_self():
    db_session = Session()

    account = db_session.query(
        Account
        ).filter_by(id=user_session['user_id']).first()
    if account.student:
        student = account.student.student
        return render_template('wizards.html', student=student)
    else:
        abort(404)


@wizards_blueprint.route('/<int:student_id>/')
@login_required
def view_students(id):
    # TODO: complete this function
    return render_template('wizards.html')


@wizards_blueprint.route('/<int:id>/', methods=['PUT'])
@login_required
def edit_student(id):
    # TODO: complete this function
    return render_template('wizards.html')


@wizards_blueprint.route('/results/')
@login_required
def search_students():
    # TODO: complete this function
    return render_template('wizards.html')
