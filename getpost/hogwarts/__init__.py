""":mod:`getpost.hogwarts` --- Controller module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from collections import namedtuple

from flask import Blueprint, render_template

from ..orm import Session


ACCOUNT_PER_PAGE = 20

# Permissions
SELF_NONE = 0x0
SELF_READ = 0x1
SELF_WRIT = 0x2
SELF_REWR = 0x3
ALLL_READ = 0x4
ALLL_WRIT = 0x5
ALLL_REWR = 0x6


def update_model(model, identifier_key, identifier_value, **kwargs):
    """Update model instance.

    Args:
        model (:cls:`getpost.orm.ReprBase`): Model to update.
        identifier_key (str): Key to query model.
        identifier_value (str): Value to query model.
        **kwargs: attribute keys and values to update.

    Returns:
        row_count (int): number of rows affected by update.

    """
    db_session = Session()
    row_count = db_session.query(
        model
        ).filter_by(**{identifier_key: identifier_value}).update(
            kwargs,
            synchronize_session=False
            )
    db_session.commit()

    return row_count


def generate_student_permissions():
    Permission = namedtuple(
        'Permission',
        ['student', 'employee', 'administrator', ]
    )

    attributes = [
        'first_name',
        'last_name',
        'ocmr',
        't_number',
        'alternative_name',
        'email_address',
    ]

    permissions = {}

    for attribute in attributes:
        permissions[attribute] = Permission(
            student=SELF_READ, employee=ALLL_REWR, administrator=ALLL_REWR
            )

    return permissions

STUDENT_PERMISSIONS = generate_student_permissions()

hogwarts_blueprint = Blueprint('hogwarts', __name__, url_prefix='')


@hogwarts_blueprint.route('/')
def hogwarts_index():
    return render_template('hogwarts.html')


@hogwarts_blueprint.route('/ping')
def ping():
    return 'What the brangan.'
