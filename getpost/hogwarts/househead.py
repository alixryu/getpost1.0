""":mod:`getpost.hogwarts.househead` --- Authorization controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from functools import wraps

from flask import Blueprint, redirect
from flask import flash, request, url_for, abort
from flask.ext.login import current_user, login_required

from .. import ANONYMOUS_ROLE
from ..models import StudentRole, EmployeeRole, AdministratorRole


ANONYMOUS_ROLE = ANONYMOUS_ROLE
ADMIN_ROLE = AdministratorRole.__tablename__
EMPLOYEE_ROLE = EmployeeRole.__tablename__
STUDENT_ROLE = StudentRole.__tablename__

househead_blueprint = Blueprint('househead', __name__, url_prefix='/role')


def requires_roles(*roles):
    """Decorator for mandating role presence.

    Args:
        *roles (str): `ADMIN_ROLE`, `EMPLOYEE_ROLE`, `STUDENT_ROLE`.

    Returns:
        wrapper (func): Curried function if designated role is present in
            :class:`flask.ext.login.current_user`,
        abort (Exception): :class:`werkzeug.exceptions.Forbidden` exception if
            no designated role is present.
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.get_current_role() not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


# TODO: should be PUT
@househead_blueprint.route('/<string:role>/', methods=['GET'])
@login_required
def switch_role(role):
    """Switch roles for account to the argument `role`.

    Args:
        role (str): `ADMIN_ROLE`, `EMPLOYEE_ROLE`, `STUDENT_ROLE`.

    Returns:
        Redirect to `next` or :func:`getpost.hogwarts.hogwarts_index`
    """
    # TODO: implement, next so that the request can redirect to original page
    if current_user.switch_current_role(role):
        flash('Role has been successfully changed.', 'success')
    else:
        flash('Role could not be changed.', 'error')
    return redirect(
        request.args.get('next') or url_for('hogwarts.hogwarts_index')
        )
