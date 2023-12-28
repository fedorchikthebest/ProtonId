from data import db_session
db_session.global_init('./db/proton_id.db')

from flask import Flask
from flask_login import LoginManager
from data.db_session import db_sess
from data.users import User
from blueprints.auth.auth import auth
from blueprints.services.services import services
from config import *

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(services)

app.config['SECRET_KEY'] = SECRET_KEY


@login_manager.user_loader
def load_user(user_id):
    user = db_sess.get(User, user_id)
    return user


if __name__ == '__main__':
    app.run()
