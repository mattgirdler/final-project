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

    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    confirm = PasswordField('confirm', validators=[InputRequired()])
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    role = SelectField('role', choices=roles, validators=[InputRequired()])
    paygrade = SelectField('paygrade', choices=paygrades, validators=[InputRequired()])
    monday = StringField('monday', validators=[InputRequired()])
    tuesday = StringField('tuesday', validators=[InputRequired()])
    wednesday = StringField('wednesday', validators=[InputRequired()])
    thursday = StringField('thursday', validators=[InputRequired()])
    friday = StringField('friday', validators=[InputRequired()])
