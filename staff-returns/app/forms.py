from db import DBAccess
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, email, InputRequired
from wtforms import validators

dbManager = DBAccess()

class LoginForm(Form):
    """Login form to access pages"""

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ProjectHoursForm(Form):
    """ Form to log project hours"""

class RegisterForm(Form):
    """ Form to register an account"""
    roles = []
    for role in dbManager.select_all_roles():
        roles.append([role['title'], role['title']])

    paygrades = []
    for paygrade in dbManager.select_paygrades():
        paygrades.append([paygrade['_id'], paygrade['_id']])

    username = StringField('username', [validators.required()])
    password = PasswordField('password', [validators.required()])
    confirm = PasswordField('confirm', [validators.required()])
    firstname = StringField('firstname', [validators.required()])
    lastname = StringField('lastname', [validators.required()])
    role = SelectField('role', choices=roles, validators=[InputRequired()])
    paygrade = SelectField('paygrade', choices=paygrades, validators=[InputRequired()])
    workingpattern = RadioField('workingpattern', choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time')], validators=[InputRequired()])
    monday = StringField('monday')
    tuesday = StringField('tuesday')
    wednesday = StringField('wednesday')
    thursday = StringField('thursday')
    friday = StringField('friday')
