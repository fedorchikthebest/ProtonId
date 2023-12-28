from flask import Blueprint, redirect
from forms.login_form import LoginForm
from flask_login import login_user, logout_user
from data.db_session import db_sess, global_init
from data.users import User
import click
import csv
import random
import string

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static', url_prefix='auth')


@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@auth.cli.command("register-from-csv")
@click.argument("csv_file")
def register_csv(csv_file):
    if db_sess is None:
        global_init('db/sea_battel.db')
    with open(csv_file) as f:
        user_data = []
        file = csv.DictReader(f)
        for i in file:
            login = f"{i.get('name')}_{i.get('sure_name')}-{random.randint(0, 10000)}"
            user = User(
                login=login,
                sure_name=i.get('sure_name'),
                second_name=i.get('second_name'),
                class_num=i.get('class_num'),
                class_liter=i.get('class_liter'),
            )
            user.set_password(''.join([random.choice(string.ascii_letters) for _ in range(8)]))
            user_data.append([])
