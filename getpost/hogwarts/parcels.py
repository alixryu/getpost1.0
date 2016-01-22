""":mod:`getpost.hogwarts.parcels` --- Package controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from datetime import datetime

from flask import Blueprint, render_template, redirect, session as user_session
from flask import abort, flash, request, url_for
from flask.ext.login import login_required

from . import update_model
from ..forms import CreatePackageForm
from ..models import Account, Package, Student
from ..orm import Session


parcels_blueprint = Blueprint('parcels', __name__, url_prefix='/packages')


@parcels_blueprint.route('/')
@login_required
def parcels_index():
    db_session = Session()

    account = db_session.query(
        Account
        ).filter_by(id=user_session['user_id']).first()
    if account.student:
        return redirect(url_for('.view_packages_self'), 303)
    else:
        return render_template('parcels.html')


@parcels_blueprint.route('/me/')
@login_required
def view_packages_self():
    """View packages designated or assigned to user.

    Args:

    Returns:
        Render template for viewing packages.

    """
    account_id = user_session['user_id']

    db_session = Session()

    account = db_session.query(
        Account
        ).filter_by(id=user_session['user_id']).first()

    base_query = db_session.query(Package)

    if account.student:
        student_id = account.student.student_info
        packages = base_query.filter_by(student_id=student_id).all()
        return render_template('parcels.html', packages=packages)
    elif account.employee:
        packages = base_query.filter_by(received_by=account_id).all()
        return render_template('parcels.html', packages=packages)
    else:
        abort(404)


@parcels_blueprint.route('/student/<int:student_id>/')
@login_required
def view_packages_by_student_id(student_id):
    """View packages designated to student with id ``student_id``.

    Args:
        student_id (int): Id of student to view packages of.

    Returns:
        Render template for viewing packages.
    """
    db_session = Session()
    packages = db_session.query(
        Package
        ).filter_by(student_id=student_id).all()
    return render_template('parcels.html', packages=packages)


@parcels_blueprint.route('/<int:package_id>')
@login_required
def view_package_details(package_id):
    """View package details of package with id ``package_id``.

    Args:
        package_id (int): Id of package to view details of.

    Returns:
        Render template for viewing packages details.

    """
    account_id = user_session['user_id']

    db_session = Session()
    account = db_session.query(Account).filter_by(id=account_id).first()
    package = db_session.query(Package).filter_by(id=package_id).first()
    student_id = account.student.student_info

    if ((account.student and student_id == package.student_id) or
            account.employee):
        return render_template('parcels.html', package=package)
    else:
        abort(404)


@parcels_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def create_package():
    """Create a new package instance.

    Args:

    Returns:
        Render template for creating a packages instance.
        Redirect to :func:`view_packages_self` after successful creation.

    """
    form = CreatePackageForm()

    if form.validate_on_submit():
        sender_name = form.sender_name.data
        ocmr = form.ocmr.data
        arrival_date = form.arrival_date.data

        db_session = Session()

        account = db_session.query(
            Account
            ).filter_by(id=user_session['user_id']).first()
        student = db_session.query(
            Student
            ).filter_by(ocmr=ocmr).first()
        employee = account.employee

        package = Package(
            sender_name=sender_name,
            student_id=student.id,
            arrival_date=arrival_date,
            received_by=employee.id,
            status='not_picked_up',
            last_edit_date=datetime.now()
            )

        db_session.add(package)

        db_session.commit()
        db_session.close()

        flash('Package has been added for student.', 'success')
        return redirect(url_for('.view_packages_self'))
    return render_template('sirius.html', form=form)


@parcels_blueprint.route('/<int:package_id>', methods=['PUT'])
@login_required
def edit_package(package_id):
    """Edit package details of package with id ``package_id``.

    Args:
        package_id (int): Id of package to edit details of.

    Returns:
        Redirect to :func:`view_package_details` after successful edit.

    """
    sender_name = request.form['sender_name']
    student_id = request.form['student_id']
    arrival_date = request.form['arrival_date']
    pickup_date = request.form['pickup_date']
    received_by = request.form['received_by']
    status = request.form['status']

    update_model(
        Package,
        Package.id.name,
        package_id,
        **{
            Package.sender_name.name: sender_name,
            Package.student_id.name: student_id,
            Package.arrival_date.name: arrival_date,
            Package.pickup_date.name: pickup_date,
            Package.received_by.name: received_by,
            Package.status.name: status,
            Package.last_edit_date.name: datetime.now()
            }
        )

    flash('Package has been edited.', 'success')
    return redirect(url_for('.view_package_details'), package_id=package_id)


@parcels_blueprint.route('/<int:package_id>', methods=['DELETE'])
@login_required
def delete_package(package_id):
    """Delete package instance with id ``package_id``.

    Args:
        package_id (int): Id of package to delete.

    Returns:
        Redirect to :func:`view_packages_self` after successful deletion.

    """
    # TODO: redirect to original page after deletion
    update_model(
        Package,
        Package.id.name,
        package_id,
        **{
            Package.is_deleted.name: True,
            Package.last_edit_date.name: datetime.now()
            }
        )

    flash('Package has been deleted.', 'success')
    return redirect(url_for('.view_packages_self'))
