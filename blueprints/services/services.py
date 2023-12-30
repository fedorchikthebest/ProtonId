from flask import Blueprint, redirect, render_template, url_for, request
from blueprints.services.forms.add_service_form import AddServiceForm
from data.services import Service
from data.db_session import db_sess
from flask_login import login_required, current_user
from functions.crypto import b64encrypt
from datetime import datetime
from json import dumps
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
        data = {
            'datetime': str(datetime.now()),
            'name': current_user.name,
            'sure_name': current_user.sure_name,
            'second_name': current_user.second_name,
            'class_num': current_user.class_num,
            'class_liter': current_user.class_liter,
            'login': current_user.login,
            'is_teacher': current_user.is_teacher
        }
    else:
        data = {
            'datetime': str(datetime.now()),
            'login': current_user.login,
            'is_teacher': current_user.is_teacher
        }
    form = ConfirmAuth()
    form.data.data = b64encrypt(dumps(data, ensure_ascii=False), key)
    acces_type = ['',
                  'Этот сайт получит только ваш логин и статус',
                  'Этот сайт узнает о вас ФИО, логин и класс']
    if service is None:
        return 'service not found'
    return render_template('confirm.html', form=form, eccess=acces_type[service.access_type], host=service.host_name)


@services.errorhandler(401)
def error401(error):
    print(error)
    return redirect(url_for('auth.login', service_id=request.url.split('/')[-1]))


