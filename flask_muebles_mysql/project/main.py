from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from . import db
import logging
from datetime import datetime
from .models import users_roles,Role

main = Blueprint('main', __name__)



#Definimos la ruta a la página principal
@main.route('/')
def index():
    logging.debug(' Fecha y Hora: {} - Arranque de la aplicacion '.format(datetime.now()))
    #print(cuerpo)
    return render_template('security/login.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
@roles_accepted('admin','vendedor','almacenista')#autorización para el rol admin
def index_login():
    roles = db.session.query(users_roles).all()
    rol_pro ={}
    for rol in roles:
        if rol[0] == current_user.id:
            rol_prop = db.session.query(Role).filter(Role.id==rol[1]).first()
            rol_pro['idRol'] = rol_prop.id
            rol_pro['descrip']=rol_prop.description
            break
    return render_template('index.html', user=current_user,rol=rol_pro)
