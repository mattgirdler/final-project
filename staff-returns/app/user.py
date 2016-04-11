import calendar
from datetime import datetime
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

    def get_user(self):
        user = dbManager.select_user(self.username)
        return user

    def get_id(self):
        return self.username

    def get_role(self):
        role = dbManager.select_user_role(self.username)
        return role

    def get_workdays(self):
        workdays = dbManager.select_user_workdays(self.username)
        return workdays

    def get_paygrade(self):
        paygrade = dbManager.select_user_paygrade(self)
        return paygrade

    def calculate_monthly_hours_required(self):
        workdays = self.get_workdays()
        for day, hours in workdays:
            print(day, hours)
            len([1 for i in calendar.monthcalendar(datetime.now().year, datetime.now().month) if i[6] != 0])

    def set_password(self):
        pass

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)