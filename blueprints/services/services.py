from flask import Blueprint, redirect, render_template, request
from blueprints.services.forms.add_service_form import AddServiceForm
from data.services import Service
from data.db_session import db_sess
from flask_login import login_required, current_user
import gostcrypto
import requests
import datetime
from functions.datetime_functions import current_jule

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


@services.route('/auth')
@login_required
def auth(service_id):
    service = db_sess.get(Service, service_id)
    if service is None:
        return 'service not found'
    if service.access_type == 1:
        requests.post(f'http://host_name/protonid', data={'user_id': current_user.id}, timeout=0.2)

    if service.access_type == 2:
        requests.post(f'http://host_name/protonid', data={'user_name': current_user.name,
                                                          'user_sure_name': current_user.sure_name,
                                                          'user_second_name': current_user.second_name,
                                                          'class_num': current_jule().year - current_user.creation_year,
                                                          'class_liter': current_user.class_liter},
                      timeout=0.2)
