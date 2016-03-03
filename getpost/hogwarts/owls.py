""":mod:`getpost.hogwarts.owls` --- Email notification controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from datetime import datetime
from threading import Thread

from flask import Blueprint, current_app, flash, redirect, render_template
from flask import url_for, abort
from flask.ext.login import login_required, current_user as account
from flask.ext.mail import Message

from .. import mail
from ..models import Notification, Package
from ..orm import Session
from .househead import requires_roles, EMPLOYEE_ROLE, STUDENT_ROLE


owls_blueprint = Blueprint('owls', __name__, url_prefix='/email')


@owls_blueprint.route('/')
@login_required
def owls_index():
    return render_template('owls.html')


@owls_blueprint.route('/<int:package_id>/', methods=['POST'])
@login_required
@requires_roles(EMPLOYEE_ROLE)
def send_notification(package_id):
    """Send e-mail and create a :class:`getpost.models.Notification` object.

    Args:
        package_id (int): Id of package to send an e-mail notification of.

    Returns:
        Redirect to :func:`view_notifications`

    """
    db_session = Session()

    package = db_session.query(Package).filter_by(id=package_id).first()
    student = package.student

    sender_name = package.sender_name

    notification_count = len(package.notifications) + 1
    email_address = student.email_address
    first_name = student.first_name

    notification = Notification(
        package_id=package_id,
        email_address=email_address,
        send_date=datetime.now(),
        send_count=notification_count)

    db_session.add(notification)

    db_session.commit()
    db_session.close()

    send_email(
        email_address,
        'You\'ve got mail.',
        'email/notification',
        package_id=package_id,
        name=first_name,
        notification_count=notification_count,
        sender=sender_name
        )

    flash(
        'Notification email number {} has been sent to student.'.format(
            notification_count
            ), 'success'
        )
    return redirect(url_for('.view_notifications', package_id=package_id))


@owls_blueprint.route('/<int:package_id>/')
@login_required
@requires_roles(EMPLOYEE_ROLE, STUDENT_ROLE)
def view_notifications(package_id):
    """View notifications of package with package id ``package_id``.

    Args:
        package_id (int): Id of package to view an e-mail notifications of.

    Returns:
        Redirect to :func:`view_notifications_self` if requested by student
        role.
        Render template to display notifications otherwise.

    """
    db_session = Session()

    if account.get_current_role() == STUDENT_ROLE:
        return redirect(
            url_for('.view_notifications_self', package_id=package_id)
            )
    notifications = db_session.query(
        Notification
        ).filter_by(package_id=package_id).all()
    return render_template('owls.html', notifications=notifications)


@owls_blueprint.route('/me/<int:package_id>/')
@login_required
@requires_roles(STUDENT_ROLE)
def view_notifications_self(package_id):
    """View notifications of package with package id ``package_id``.

    Args:
        package_id (int): Id of package to view an e-mail notifications of.

    Returns:
        Render template to display notifications.

    """
    db_session = Session()
    package = db_session.query(
        Package
        ).filter_by(id=package_id).first()
    if account.student.student_info != package.student_id:
        abort(403)
    notifications = db_session.query(
        Notification
        ).filter_by(package_id=package_id).all()
    return render_template('owls.html', notifications=notifications)


def send_email(to, subject, template, **kwargs):
    """Send asynchronous e-mail with flask-mail.

    Send an asynchronous e-mail to address ``to`` with subject ``subject``
    using either a txt or html file type template ``template``. Arguments for
    the template are accepted by ``**kwargs``.

    Args:
        to (str): E-mail address of recipient.
        subject (str): Subject of e-mail.
        template (str): Path to template from the default templates
            directory of the flask project.
        **kwargs: Arguments for template.

    Returns:
        thr: :class:`threading.Thread` sending e-mail.

    """
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=_send_async_email, args=[app, msg])
    thr.start()
    return thr


def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
