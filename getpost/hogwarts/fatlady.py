""":mod:`getpost.hogwarts.fatlady` --- Authentication controller module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import Blueprint, render_template, redirect, session as user_session
from flask import flash, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from ..orm import Session
from ..forms import LoginForm, SignupForm
from ..models import Account, Student, StudentRole


fatlady_blueprint = Blueprint('fatlady', __name__, url_prefix='/auth')


@fatlady_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Log in with e-mail address and password.

    This function is set by flask-login's ``LoginManager`` in this project's
    ``create_app`` factory as the view function to redirect to when a user
    needs to log in. When redirected in this way, flask-login creates a
    ``next`` argument in the url query string to redirect back to after
    successful authentication.

    Args:

    Returns:
        Render template for signing in.
        Redirect to ``next`` or home after successful authentication.

    """
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        if authenticate_user(email, password, remember_me):
            flash('Login succeeded!', 'success')
            return redirect(
                request.args.get('next') or url_for('hogwarts.hogwarts_index')
                )
        flash('Invalid Login.', 'error')
    return render_template('fatlady.html', form=form)


def authenticate_user(email, password, remember_me):
    """Authenticate user with e-mail address and password.

    Args:
        email (str): E-mail address to authenticate with.
        password (str): password to authenticate with.
        remember_me (bool): Stay-signed-in option.

    Returns:
        account (:clsss:`getpost.models.Account`): Account object of
            authenticated account. Returns `None` if not authenticated.

    """
    db_session = Session()

    account = db_session.query(
        Account
        ).filter_by(email_address=email).first()

    if account is not None and account.check_password(password):
        account.log_in()
        login_user(account, remember_me)
        return account
    else:
        return None


@fatlady_blueprint.route('/logout/', methods=['GET'])
@login_required
def logout():
    """Log out of current log in session.

    Args:

    Returns:
        Redirect to home after successful logging out.

    """
    deauthenticate_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('hogwarts.hogwarts_index'))


def deauthenticate_user():
    """Deauthenticate current account.

    Args:

    Returns:

    """
    db_session = Session()
    account = db_session.query(
        Account
        ).filter_by(id=user_session['user_id']).first()
    account.log_out()
    logout_user()


@fatlady_blueprint.route('/signup/student/', methods=['GET', 'POST'])
def signup():
    """Sign up and create a new account.

    This function creates a new ``Acount`` instance as well as a
    ``StudentRole`` instance.

    Args:

    Returns:
        Render template for signing up.
        Redirect to :func:`login` after successful signing up.

    """
    form = SignupForm()

    if form.validate_on_submit():
        email = form.email.data
        t_number = form.t_number.data
        password = form.password.data
        password2 = form.password2.data

        if password != password2:
            flash('Passwords do not match.', 'error')
            return render_template('sortinghat.html', form=form)

        result = create_account(email, t_number, password)

        if result == 1:
            flash('You can now login.', 'success')
            return redirect(url_for('fatlady.login'))
        elif result == -1:
            flash('Account already exists with this email address.', 'error')
        else:  # result == 0
            flash('There exists no matching student information.', 'error')
    return render_template('sortinghat.html', form=form)


def create_account(email, t_number, password):
    """Create a new :class:`getpost.models.Account`, with a new
        :class:`getpost.models.StudentRole`.

    Args:
        email (str): E-mail address to create account with.
        t_number (str): T Number to create account with.
        password (str): password to create account with.

    Returns:
        (int):
            1: successful creation of account.
            0: unsuccessful creation (no matching student information).
            -1: unsuccessful creation (already existing account).

    """
    db_session = Session()

    # check if account already exists
    repeat_account = db_session.query(
            Account
            ).filter_by(email_address=email).first()
    if repeat_account:
        return -1
    # find matching student instance
    student = db_session.query(
        Student
        ).filter_by(email_address=email, t_number=t_number).first()

    if student:  # match exists
        student_id = student.id
        student_first_name = student.first_name
        student_last_name = student.last_name

        # create new account
        account = Account(
            email_address=email,
            verified=True,
            role='student'
            )
        account.set_password(password)
        db_session.add(account)
        db_session.commit()

        # bring back account
        account = db_session.query(
            Account
            ).filter_by(email_address=email).first()

        # create new student role
        student_role = StudentRole(
            account_id=account.id,
            first_name=student_first_name,
            last_name=student_last_name,
            student_info=student_id
            )

        db_session.add(student_role)
        db_session.commit()

        return 1
    else:  # no match exists
        return 0
