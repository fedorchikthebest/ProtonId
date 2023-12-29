from flask import Blueprint, redirect, render_template, url_for
from blueprints.services.forms.add_service_form import AddServiceForm
from data.services import Service
from data.db_session import db_sess
from flask_login import login_required, current_user
from functions.crypto import b64encrypt
from blueprints.services.forms.confirm_auth import ConfirmAuth

services = Blueprint('services', __name__, template_folder='templates',
                     static_folder='static', url_prefix='/service')


@services.route('/add', methods=['GET', 'POST'])
@login_required
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        new_service = Service(
            owner_id=current_user.id,
            kuznechik_key=form.kuznechik_key.data,
            host_name=form.host.data,
            access_type=form.access_type.data
        )
        db_sess.add(new_service)
        db_sess.commit()
        return redirect('/')
    return render_template('add_service.html', form=form)


@services.route('/auth/<string:service_id>', methods=['GET', 'POST'])
@login_required
def auth(service_id):
    service = db_sess.get(Service, service_id)
    key = service.kuznechik_key
    if service.access_type == 2:
        form = ConfirmAuth(
            name=b64encrypt(current_user.name, key),
            test_key=b64encrypt('FEDOR_GORLENKO', key),
            sure_name=b64encrypt(current_user.sure_name, key),
            second_name=b64encrypt(current_user.second_name, key),
            class_num=b64encrypt(current_user.class_num, key),
            class_liter=b64encrypt(current_user.class_liter, key),
            login=b64encrypt(current_user.login, key)
        )
    else:
        form = ConfirmAuth(
                            login=b64encrypt(current_user.login, key),
                           test_key=b64encrypt('FEDOR_GORLENKO', key),)
    acces_type = ['',
                  'Этот сайт получит только ваш логин',
                  'Этот сайт узнает о вас ФИО, логин и класс']
    if service is None:
        return 'service not found'
    return render_template('confirm.html', form=form, eccess=acces_type[service.access_type], host=service.host_name)


@services.errorhandler(401)
def error401(error):
    return redirect(url_for('auth.login'))


