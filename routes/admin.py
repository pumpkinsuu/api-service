from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from database import KeyData
from config.admin import *


def create_admin_bp(app):
    admin_bp = Blueprint('admin_bp', __name__)

    db = KeyData(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == USERNAME:
            return User(user_id)
        return None

    class User(UserMixin):
        def __init__(self, user_id):
            self.id = user_id

        def get(self):
            return self.id

    @admin_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == USERNAME and password == PASSWORD:
                user = User(USERNAME)
                login_user(user)
                return redirect(url_for('admin_bp.main'))
            flash('Invalid username or password', 'warn')

        return render_template('loginPage.html')

    @admin_bp.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('admin_bp.login'))

    @admin_bp.route('/')
    @login_required
    def main():
        data = db.get()
        return render_template('mainPage.html', data=data)

    @admin_bp.route('/moodle', methods=['GET', 'POST'])
    @login_required
    def create():
        if request.method == 'POST':
            name = request.form.get('name')
            moodle = request.form.get('moodle')
            wstoken = request.form.get('wstoken')
            key = request.form.get('key')

            if moodle[-1] == '/':
                moodle = moodle[:-1]

            if db.get_by_name(name):
                flash('Name exist!', 'warn')
            elif db.get_data(moodle):
                flash('Moodle exist!', 'warn')
            elif db.create(
                name=name,
                moodle=moodle,
                wstoken=wstoken,
                key=key
            ):
                flash('Created', 'info')
                return redirect(url_for('admin_bp.update', name=name))
            else:
                flash('Failed to create', 'error')
        return render_template('addPage.html')

    @admin_bp.route('/moodle/<name>', methods=['GET', 'POST'])
    @login_required
    def update(name):
        if request.method == 'POST':
            moodle = request.form.get('moodle')
            wstoken = request.form.get('wstoken')
            key = request.form.get('key')
            if db.update(
                name=name,
                moodle=moodle,
                wstoken=wstoken,
                key=key
            ):
                flash('Updated', 'info')
            else:
                flash('Failed to update', 'error')

        data = db.get_by_name(name)
        if not data:
            abort(404)
        return render_template('editPage.html', data=data)

    @admin_bp.route('/moodle/<name>/remove', methods=['POST'])
    @login_required
    def remove(name):
        if db.remove(name):
            flash('Removed', 'info')
            return redirect(url_for('admin_bp.main'))
        else:
            flash('Failed to remove', 'error')
            return redirect(url_for('admin_bp.update', name=name))

    @admin_bp.route('/search')
    @login_required
    def search():
        keyword = request.args.get('keyword')
        data = db.search(keyword)
        flash(f'{len(data)} results', 'info')
        return render_template('mainPage.html', data=data)

    return admin_bp
