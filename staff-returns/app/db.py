from pymongo import MongoClient
from tasks import sort_monthly_projects, calculate_hours_required
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import json
import operator


class DBAccess():

    def __init__(self):

        self._connection = self._connect_to_db()

    def _connect_to_db(self):

        client = MongoClient()
        return client.test

    def get_collection(self, collection_name):
        return self._connection[collection_name]

    """ User Functions """

    def select_user(self, user_id):
        collection = self.get_collection('users')
        user = collection.find_one({'_id': user_id})

        if user:
            # Prepare user for data entry
            date = datetime.now()
            year = str(date.year)
            month = date.strftime("%B")
            if year not in user:
                user[year] = {}
            if month not in user[year]:
                user[year][month] = {}
                user[year][month]['projects'] = {}
            if 'total_hours' not in user[year][month]:
                user[year][month]['total_hours'] = 0
            if 'hours_required' not in user[year][month] or user[year][month]['hours_required'] == 0:
                hours_required = calculate_hours_required(user['workdays'])
                user[year][month]['hours_required'] = hours_required
            self.update_user(user)
            return user
        else:
            return 'User not found'

    def insert_user(self, user):
        collection = self.get_collection('users')
        user_dict = {
            '_id': str.upper(user.username.data),
            'firstname': user.firstname.data.title(),
            'lastname': user.lastname.data.title(),
            'password': generate_password_hash(user.password.data),
            'role': user.role.data,
            'paygrade': user.paygrade.data,
            'workdays': {"Monday": "0", "Tuesday": "0", "Wednesday": "0", "Thursday": "0", "Friday": "0"}
        }
        try:
            collection.insert_one(user_dict)
            return "Success"
        except Exception as e:
            return "Fail"

        # Log the user's monthly hours to the Users table
    def log_hours_for_user(self, user_id, sorted_projects):
        collection = self.get_collection('users')
        user = self.select_user(user_id)
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        user = self.clear_hours_for_user(user)
        project_dict = {}
        for k,v in sorted_projects.items():
            project_id = self.select_project_id_from_name(k)
            project_dict[project_id] = sorted_projects[k]
        if year not in user:
            user[year] = {}
        if month not in user[year]:
            user[year][month] = {}
            user[year][month]['projects'] = {}
        if 'total_hours' not in user[year][month]:
            user[year][month]['total_hours'] = 0
        for k,v in project_dict.items():
            user[year][month]['projects'][k] = v
        user[year][month]['total_hours'] = self.update_user_total_hours(user)
        collection.replace_one({"_id": user_id}, user)
        return user

    def clear_hours_for_user(self, user):
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        monthly_projects = []
        try:
            for k, v in user[year][month]['projects'].items():
                monthly_projects.append(k)
                self.clear_hours_for_project(user, k)
            for item in monthly_projects:
                user[year][month]['projects'].pop(item, None)
        except Exception as e:
            print(str(e))
        return user

    def update_user_total_hours(self, user):
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        total_hours = 0
        for project in user[year][month]['projects']:
            total_hours += float(user[year][month]['projects'][project])
        return total_hours

    def update_user(self, user):
        collection = self.get_collection('users')
        collection.replace_one({"_id": user['_id']}, user)

    def select_all_roles(self):
        collection = self.get_collection('roles')
        roles = collection.find()
        role_list = []
        for role in roles:
            role_list.append(role)
        role_list.sort(key=operator.itemgetter('title'))
        return role_list

    def select_user_hourly_rate(self, user_id):
        collection = self.get_collection('paygrades')
        user = self.select_user(user_id)
        paygrade = user['paygrade']
        paygrade = collection.find_one({'_id': paygrade})
        return paygrade['hourly_rate']


    """ Project Functions """

    def log_projects(self, user_id, form_data):
        sorted_projects = sort_monthly_projects(form_data)
        if sorted_projects != {}:
            self.log_hours_for_user(user_id, sorted_projects)
            self.log_hours_for_project(user_id, sorted_projects)
            return "Hours logged successfully"
        else:
            return "No projects entered"

    # Log the user's monthly hours to the Projects table
    def log_hours_for_project(self, user_id, sorted_projects):
        collection = self.get_collection('projects')
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        hourly_rate = self.select_user_hourly_rate(user_id)
        print(hourly_rate)
        for k,v in sorted_projects.items():
            project_id = self.select_project_id_from_name(k)
            project = self.select_project(project_id)
            if not project.get(year):
                project[year] = {}
            if not project[year].get(month):
                project[year][month] = {}
                project[year][month]['users'] = {}
            if 'total_hours' not in project[year][month]:
                project[year][month]['total_hours'] = 0
            project[year][month]['users'][user_id] = {}
            project[year][month]['users'][user_id]['hours'] = v
            project[year][month]['users'][user_id]['cost'] = float(hourly_rate) * float(v)
            project[year][month]['total_hours'] = self.update_project_total_hours(project)
            project[year][month]['total_cost'] = self.update_project_total_cost(project)
            collection.replace_one({"_id": project_id}, project)

    def update_project_total_hours(self, project):
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        total_hours = 0
        for user in project[year][month]['users']:
            total_hours += float(project[year][month]['users'][user]['hours'])
        return total_hours

    def update_project_total_cost(self, project):
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        total_cost = 0
        for user in project[year][month]['users']:
            total_cost += float(project[year][month]['users'][user]['cost'])
        return total_cost

    def select_project_id_from_name(self, project_name):
        collection = self.get_collection('projects')
        cursor = collection.find({"name": project_name})
        project = cursor.next()
        project_id = project['_id']
        return project_id

    def select_project(self, project_id):
        collection = self.get_collection('projects')
        project = collection.find_one({ '_id': project_id })
        return project

    def select_all_projects(self):
        collection = self.get_collection('projects')
        projects = collection.find()
        project_list = []
        for project in projects:
            project_list.append(project)
        project_list.sort(key=operator.itemgetter('name'))
        return project_list

    def clear_hours_for_project(self, user, project_id):
        collection = self.get_collection('projects')
        project = self.select_project(project_id)
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        project[year][month]['users'][user['_id']] = {}
        collection.replace_one({'_id': project_id}, project)

    def set_password(self, user_id, password):
        collection = self.get_collection('users')
        hashed_password = generate_password_hash(password)
        collection.update_one({'_id': user_id}, {'$set': {'password': hashed_password}})

    def select_user_workdays(self, user_id):
        user = self.select_user(user_id)
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        try:
            workdays = user['workdays']
            sorted_workdays = []
            for day in weekdays:
                sorted_workdays.append([day, workdays[day]])
                print(day)
            return sorted_workdays
        except Exception as e:
            print ('No workdays found for' + user_id)
            return [['Monday', '0'], ['Tuesday', '0'], ['Wednesday', '0'], ['Thursday', '0'], ['Friday', '0']]

    def select_user_role(self, user_id):
        user = self.select_user(user_id)
        try:
            role = user['role']
            return role
        except Exception as e:
            print('No ' + str(e) + ' found for ' + user_id)
            return None

    def select_user_paygrade(self, user):
        user = self.select_user(user.username)
        try:
            paygrade = user['paygrade']
            return paygrade
        except Exception as e:
            print('No ' + str(e) + ' found for ' + user.username)
            return None

    def select_paygrades(self):
        collection = self.get_collection('paygrades')
        paygrades = collection.find()
        paygrade_list = []
        for paygrade in paygrades:
            paygrade_list.append(paygrade)
        paygrade_list.sort(key=operator.itemgetter('_id'))
        return paygrade_list

    def set_role(self, user_id, form_data):
        collection = self.get_collection('users')
        form_data_dict = form_data.to_dict()
        role = form_data_dict['role']
        if role != 'Select your role':
            collection.update_one({'_id': user_id}, {'$set': {'role': role}})
        return form_data_dict

    def set_working_hours(self, user_id, form_data):
        collection = self.get_collection('users')
        form_data_dict = form_data.to_dict()
        workdays = {}
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in weekdays:
            workdays[day] = form_data_dict[day]
        collection.update_one({'_id': user_id}, {'$set': {'workdays': workdays}})