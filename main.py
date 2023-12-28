from data import db_session
db_session.global_init('./db/proton_id.db')

from flask import Flask
from flask_login import LoginManager
from data.db_session import db_sess
from data.users import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = db_sess.get(User, user_id)
    return user