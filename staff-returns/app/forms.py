from db import DBAccess
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, RadioField, DecimalField
from wtforms.validators import DataRequired, EqualTo, email, InputRequired, NumberRange
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
    paygrade = SelectField('paygrade', choices=paygrades, validators=[InputRequired()])
    monday = DecimalField('monday', validators=[InputRequired()])
    tuesday = DecimalField('tuesday', validators=[InputRequired()])
    wednesday = DecimalField('wednesday', validators=[InputRequired()])
    thursday = DecimalField('thursday', validators=[InputRequired()])
    friday = DecimalField('friday', validators=[InputRequired()])
