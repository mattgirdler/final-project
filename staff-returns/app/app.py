from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
app.secret_key = 'secret key'
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
