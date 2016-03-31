from db import DBAccess
from werkzeug.security import check_password_hash, generate_password_hash

dbManager = DBAccess()

class User():

    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def get_roles(self):
        roles = dbManager.get_user_roles(self.username)
        return roles

    def set_password(self):
        pass

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)