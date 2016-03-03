""":mod:`getpost.forms` --- WTForms module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms import SelectField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.fields.html5 import DateTimeLocalField, EmailField
from wtforms.validators import EqualTo, Regexp, Required


class CreatePackageForm(Form):
    sender_name = StringField('Sender Name: ', validators=[Required()])
    ocmr = StringField(
        'Student OCMR: ',
        validators=[
            Required(),
            Regexp('^[0-9]{4}$', message='Please enter a four digit OCMR')
            ]
        )
    arrival_date = DateTimeLocalField(
        'Arrival Time: ', validators=[Required()]
        )
    submit = SubmitField('Register Package')


class LoginForm(Form):
    email = EmailField(
        'Email',
        validators=[
            Required(),
            Regexp(
                '[a-zA-Z0-9]+@oberlin.edu',
                message='Please enter an Oberlin e-mail account'
                )
            ]
        )
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Stay logged in')
    submit = SubmitField('Log In')


class SignupForm(Form):
    email = EmailField(
        'Email',
        validators=[
            Required(),
            Regexp(
                '[a-zA-Z0-9]+@oberlin.edu',
                message='Please enter an Oberlin e-mail account'
                )
            ]
        )
    t_number = StringField(
        'T Number',
        validators=[
            Required(),
            Regexp('T?[0-9]{8}')
            ]
        )
    password = PasswordField(
        'Password',
        validators=[
            Required(), EqualTo('password2', message='Passwords must match.')
            ]
        )
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')


class StudentSearchForm(Form):
    query = StringField(
        'Search Keywords'
        )
    submit = SubmitField('Search')


def ModelForm(model, db_session, exclude=None):
    return model_form(
        model=model,
        db_session=db_session,
        base_class=Form,
        exclude_fk=False,
        exclude=exclude
        )


class EditPackageForm(Form):
    sender_name = StringField('Sender')
    arrival_date = DateTimeLocalField('Arrival Date')
    pickup_date = DateTimeLocalField('Pick Up Date')
    status = SelectField(
        'Status',
        choices=[
            (
                'picked_up',
                'Picked up'
                ),
            (
                'not_picked_up',
                'Not picked up'
                )
            ]
        )
    student = StringField('Student')
    employee = StringField('Employee')
    # notifications =
