from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user
from . models import User
from . import db, userDataStore
import logging
from datetime import datetime 

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login', methods=['GET'])
def login():
    try:
        return render_template('/security/login.html')
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@auth.route('/login', methods=['POST'])
def login_post():
    try:
    
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        #Consultamos si existe un usuario ya registrado con el email.
        user = User.query.filter_by(email=email).first()
        print(user)
        if not user or not check_password_hash(user.password, password):
            flash('El usuario y/o la contraseña son incorrectos')
            return redirect(url_for('auth.login')) 
        
        login_user(user, remember=remember)
        
        logging.debug(' Fecha y Hora: {} - Usuario: {} y Contraseña: {} correctos, inicio se sesion exitoso '.format(datetime.now(),email, password))
        return redirect(url_for('main.index_login'))
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')


@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('main.index'))
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
