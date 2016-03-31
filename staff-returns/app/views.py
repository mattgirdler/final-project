from app import app, lm
from flask import Flask, render_template, request, url_for, flash, redirect
from datetime import datetime
from db import DBAccess
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RoleForm
from user import User
import json

dbManager = DBAccess()

@app.route("/", methods=['GET', 'POST'])
@login_required
def main():

    if request.method == 'GET':
        user = load_user(current_user.username)
        user_roles = user.get_roles()
        date = datetime.now()
        year = str(date.year)
        month = date.strftime("%B")
        projects = dbManager.select_all_projects()
        return render_template(
            'staff-returns.html',
            title='home',
            month=month,
            year=year,
            projects=projects,
            user_roles=user_roles
        )
    else:
        form_data = request.form
        result = dbManager.log_projects(current_user.username, form_data)
        return str(result)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = load_user(current_user.username)
    user_roles = user.get_roles()
    form = RoleForm()
    if request.method == 'POST':
        form_data = request.form
        result = dbManager.set_role(user.username, form_data)
        return str(result)
    roles = dbManager.select_all_roles()
    return render_template('user-settings.html',
                           title='settings',
                           roles=roles,
                           form=form,
                           user_roles=user_roles)


@app.route('/project-management', methods=['GET'])
@login_required
def project_management():
    user = load_user(current_user.username)
    user_roles = user.get_roles()
    if "Admin" in user_roles:
        projects = dbManager.select_all_projects()
        return render_template('project-management.html',
                               title='project-management',
                               user_roles=user_roles,
                               projects=projects)
    else:
        return render_template('404.html'), 404


@app.route('/load-project/<project_name>', methods=['GET'])
@login_required
def load_project(project_name=None):
    user = load_user(current_user.username)
    user_roles = user.get_roles()
    if "Admin" in user_roles:
        project_id = dbManager._get_project_id_from_name(project_name)
        project = dbManager.select_project(project_id)
        return json.dumps(project)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = dbManager.select_user(form.username.data)
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully", category='success')
            return redirect(request.args.get("next") or url_for('main'))
        flash("Wrong username or password", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated():
        user = load_user(current_user.username)
        user_roles = user.get_roles()
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