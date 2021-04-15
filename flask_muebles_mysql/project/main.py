from flask import Blueprint, render_template,request
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from . import db
import logging
from datetime import datetime
from .models import users_roles,Role

main = Blueprint('main', __name__)


@main.route('/')
def index():
    try:
        return render_template('security/login.html')
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
@roles_accepted('admin','vendedor','almacenista')#autorización para el rol admin
def index_login():
    try:
        return render_template('index.html', user=current_user)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

