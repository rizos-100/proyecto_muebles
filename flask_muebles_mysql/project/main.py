from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from . import db
import logging
from datetime import datetime
from .models import  personaSchema,persona,User

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
    perUser = db.session.query(persona,User).join(User.personaForeign).filter(User.id==current_user.id).first()
        
    return render_template('index.html', user=perUser)
