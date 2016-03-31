from pymongo import MongoClient
from tasks import sort_monthly_projects
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

    def _get_collection(self, collection_name):
        return self._connection[collection_name]

    def select_user(self, user_id):
        collection = self._get_collection('users')
        user = collection.find_one({ '_id': user_id })
        return user

    def select_project(self, project_id):
        collection = self._get_collection('projects')
        project = collection.find_one({ '_id': project_id })
        return project

    def select_all_projects(self):
        collection = self._get_collection('projects')
        projects = collection.find()
        project_list = []
        for project in projects:
            project_list.append(project)
        project_list.sort(key=operator.itemgetter('name'))
        return project_list

    def select_all_roles(self):
        collection = self._get_collection('roles')
        roles = collection.find()
        role_list = []
        for role in roles:
            role_list.append(role)
        role_list.sort(key=operator.itemgetter('title'))
        return role_list


    def log_projects(self, user_id, form_data):
        sorted_projects = sort_monthly_projects(form_data)
        user = self.log_hours_for_user(user_id, sorted_projects)
        self.log_hours_for_project(user_id, sorted_projects)
        return user


    def log_hours_for_user(self, user_id, sorted_projects):
        collection = self._get_collection('users')
        user = self.select_user(user_id)
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        user = self._clear_monthly_projects(user)
        project_dict = {}
        for k,v in sorted_projects.items():
            project_id = self._get_project_id_from_name(k)
            project_dict[project_id] = sorted_projects[k]

        if year not in user:
            user[year] = {}
        if month not in user[year]:
            user[year][month] = {}

        for k,v in project_dict.items():
            user[year][month][k] = v

        collection.replace_one({ "_id": user_id }, user)
        return user


    def log_hours_for_project(self, user_id, sorted_projects):
        collection = self._get_collection('projects')
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        for k,v in sorted_projects.items():
            project_id = self._get_project_id_from_name(k)
            project = self.select_project(project_id)
            if year not in project:
                project[year] = {}
            if month not in project[year]:
                project[year][month] = {}
            project[year][month][user_id] = v
            print(project)
            collection.replace_one({ "_id": project_id }, project)


    def _get_project_id_from_name(self, project_name):
        collection = self._get_collection('projects')
        cursor = collection.find( { "name": project_name } )
        project = cursor.next()
        project_id = project['_id']
        return project_id

    def _clear_monthly_projects(self, user):
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        monthly_projects = []
        try:
            for k,v in user[year][month].items():
                monthly_projects.append(k)
            for item in monthly_projects:
                user[year][month].pop(item, None)
        except Exception as e:
            print(str(e))
        return(user)


    def set_password(self, user_id, password):
        collection = self._get_collection('users')
        hashed_password = generate_password_hash(password)
        collection.update_one( { '_id': user_id }, {'$set': { 'password': hashed_password } })


    def get_user_roles(self, user_id):
        user = self.select_user(user_id)
        try:
            roles = user['role']
            return roles
        except Exception as e:
            print('No ' + str(e) + ' found for ' + user_id)
            return None


    def set_role(self, user_id, form_data):
        collection = self._get_collection('users')
        form_data_dict = form_data.to_dict()
        role = form_data_dict['role']
        if role != 'Select your role':
            collection.update_one( { '_id': user_id }, {'$set': { 'role': role } })
        return form_data_dict