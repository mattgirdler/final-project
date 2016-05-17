from app import app, lm
from flask import Flask, render_template, request, url_for, flash, redirect
from datetime import datetime
from db import DBAccess
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegisterForm
from user import User
import json

dbManager = DBAccess()

@app.route("/", methods=['GET', 'POST'])
@login_required
def main():
    result = None
    if request.method == 'POST':
        form_data = request.form
        result = dbManager.log_projects(current_user.username, form_data)
        if result == "Hours updated successfully":
            flash(result, 'success')
        elif result == "No projects entered":
            flash(result, 'error')
    sorted_user_projects = {}
    total_hours = 0
    hours_required = 0
    date = datetime.now()
    year = str(date.year)
    month = date.strftime("%B")
    user = load_user(current_user.username)
    user_role = user.get_role()
    user_dict = dbManager.select_user(user.username)
    if year in user_dict and month in user_dict[year]:
        user_projects = user_dict[year][month]['projects']
        for x, y in user_projects.items():
            project = dbManager.select_project(x)
            sorted_user_projects[project['name']] = user_projects[x]
            print(sorted_user_projects)
        if 'total_hours' in user_dict[year][month]:
            total_hours = int(user_dict[year][month]['total_hours'])
        if 'hours_required' in user_dict[year][month]:
            hours_required = int(user_dict[year][month]['hours_required'])
    projects = dbManager.select_all_projects()
    return render_template(
        'staff-returns.html',
        title='home',
        month=month,
        year=year,
        projects=projects,
        user_role=user_role,
        user_projects=sorted_user_projects,
        total_hours=total_hours,
        hours_required=hours_required,
        result=result)


@app.route('/budget-tracking', methods=['GET'])
@login_required
def project_management():
    user = load_user(current_user.username)
    user_role = user.get_role()
    users = dbManager.select_all_users();
    date = datetime.now()
    year = str(date.year)
    month = date.strftime("%B")
    monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    if user_role == 'Admin' or user_role == 'Delivery Manager':
        projects = dbManager.select_all_projects()
        return render_template('budget-tracking.html',
                               title='budget-tracking',
                               user_role=user_role,
                               projects=projects,
                               monthNames=monthNames,
                               current_month=month,
                               current_year=year,
                               users=users)
    else:
        return render_template('404.html'), 404

@app.route('/user-management', methods=['GET', 'POST'])
@login_required
def user_management():
    result = None
    if request.method == 'POST':
        form_data = request.form
        result = dbManager.update_user(form_data)
        if result == "User updated successfully":
            flash(result, 'success')
    user = load_user(current_user.username)
    user_role = user.get_role()
    if user_role == 'Admin':
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        roles = dbManager.select_all_roles()
        paygrades = dbManager.select_paygrades()
        users = dbManager.select_all_users()
        return render_template('user-management.html',
                               days=days,
                               paygrades=paygrades,
                               roles=roles,
                               title='user-management',
                               users=users,
                               user_role=user_role,
                               result=result)
    else:
        return render_template('404.html'), 404


@app.route('/load-user/<user_id>', methods=['GET'])
@login_required
def load_user_data(user_id=None):
    user = load_user(current_user.username)
    user_role = user.get_role()
    if user_role == 'Admin' or user_role == 'Delivery Manager':
        user = dbManager.select_user(user_id)
        user.pop('password')
        return json.dumps(user)


@app.route('/load-project/<project_name>', methods=['GET'])
@login_required
def load_project(project_name=None):
    user = load_user(current_user.username)
    user_role = user.get_role()
    if user_role == 'Admin' or user_role == 'Delivery Manager':
        project_id = dbManager.select_project_id_from_name(project_name)
        project = dbManager.select_project(project_id)
        return json.dumps(project)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = dbManager.select_user(str.upper(form.username.data))
        if user != 'User not found':
            if user and User.validate_login(user['password'], form.password.data):
                user_obj = User(user['_id'])
                if form.remember.data:
                    login_user(user_obj, remember=True)
                else:
                    login_user(user_obj)
                flash("Logged in successfully", category='success')
                return redirect(request.args.get("next") or url_for('main'))
            else:
                flash("Wrong username or password", category='error')
        else:
            flash("Wrong username or password", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        logout_user()
    form = RegisterForm(request.form)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are required.', category='error')
        else:
            result = dbManager.insert_user(form)
            if result == 'Success':
                flash('Account created', category='success')
                return redirect(url_for('login'))
            else:
                flash('Username taken', category='error')
    return render_template('register.html', title='register', form=form, days=days)


@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated():
        user = load_user(current_user.username)
        user_roles = user.get_role()
        return render_template('404.html', user_roles=user_roles), 404
    else:
        return render_template('404.html'), 404


@lm.user_loader
def load_user(user_id):
    u = dbManager.select_user(user_id)
    if not u:
        return None
    return User(u['_id'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)