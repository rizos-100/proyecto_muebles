from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user
from . models import User
from . import db, userDataStore
import logging
from datetime import datetime 

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Consultamos si existe un usuario ya registrado con el email.
    user = User.query.filter_by(email=email).first()

    #Verificamos si el usuario existe, encriptamos el password y lo comparamos con
    # el de la BD.
    if not user or not check_password_hash(user.password, password):
        #Si el usuario no existe o no coinciden los passwords
        flash('El usuario y/o la contraseña son incorrectos')
        logging.error(' Fecha y Hora: {} - Usuario: {} y Contraseña: {} incorrectos, intento de inicio de sesion fallido '.format(datetime.now(),email, password))
        return redirect(url_for('auth.login')) 

    #En este punto el usuario tiene los datos correctos
    #Creamos una sessión y logueamso al usuario.
    login_user(user, remember=remember)
    
    logging.debug(' Fecha y Hora: {} - Usuario: {} y Contraseña: {} correctos, inicio se sesion exitoso '.format(datetime.now(),email, password))
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #Consultamos si existe un usuario ya registrado con el email.
    user = User.query.filter_by(email=email).first()

    if user: #El usuario existe y regresamos a la página de registro.
        flash('El correo ya existe')
        logging.error('Fecha y Hora: {} - El correo: {} ya existe '.format(datetime.now(),email))
        return redirect(url_for('auth.register'))

    #Creamos un nuevo usuario
    #newuser = User(email=email, name=name, 
    #password=generate_password_hash(password,method='sha256'))
    userDataStore.create_user(
        name=name, email=email, 
        password=generate_password_hash(password, method='sha256')
    )

    logging.debug(' Fecha y Hora: {} - Correo: {}, Nombre: {} y Contraseña: {} guardados correctamente'.format(datetime.now(),email,name,password))
    
    #Agregamos el usuario a la bd.
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la session
    logout_user()
    return redirect(url_for('main.index'))
