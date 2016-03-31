from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class LoginForm(Form):
    """Login form to access pages"""

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RoleForm(Form):
    """ Form to change user role"""

    role = SelectField('role_select', validators=[DataRequired()])