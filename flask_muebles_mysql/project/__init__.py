import os
from flask import Flask,render_template,request
from flask_security import Security, SQLAlchemyUserDatastore, utils, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib  import sqla
from wtforms.fields import PasswordField

import logging
from datetime import datetime

#Creamos una instancia de SQLAlchemy
db = SQLAlchemy()
#Creamos el objeto SQLalchemyUserDaaStore
from .models import User, Role, RoleAdmin, UserAdmin

userDataStore = SQLAlchemyUserDatastore(db, User, Role)

now = datetime.now()
fechaHoy = now.strftime('%Y-%m-%d')
UPLOAD_TMP = os.path.abspath('project/tmp/')
LOG_FILENAME = UPLOAD_TMP+'/errores_'+fechaHoy+'.log'

def create_app():
    #Creamos una instancia del flask
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generar la clave de sessión para crear una cookie con la inf. de la sessión
    app.config['SECRET_KEY'] = os.urandom(24)
    #Usar en caso de que no se tenga algun acceso a la principal
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u512768467_user_producci2:7=Vhafn^K9@31.170.161.1/u512768467_muebleria2'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u512768467_user_produccio:7=Vhafn^K9@31.170.161.1/u512768467_muebleria'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/muebleria'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        try:
            db.create_all()
            
            userDataStore.find_or_create_role(name='admin', description='Administrator')
            userDataStore.find_or_create_role(name='vendedor', description='Vendedor')
            userDataStore.find_or_create_role(name='almacenista', description='Almacenista')

            encrypted_password = generate_password_hash('password', method='sha512') #utils.encrypt_password('password')
            if not userDataStore.get_user('vendedor@example.com'):
                    userDataStore.create_user(email='vendedor@example.com', password=encrypted_password,
                                            numero_empleado=232,nivel_escolar='Telesecundaria',profesion='Ama de casa',
                                            observaciones='Es a toda madre',idPersona=7,estatus=1)
                    db.session.commit()
            if not userDataStore.get_user('admin@example.com'):
                userDataStore.create_user(email='admin@example.com', password=encrypted_password,
                                            numero_empleado=32,nivel_escolar='Telesecundaria',profesion='Ama de casa',
                                            observaciones='Es a toda madre',idPersona=5,estatus=1)
                db.session.commit()
            if not userDataStore.get_user('almacenista@example.com'):
                userDataStore.create_user(email='almacenista@example.com', password=encrypted_password,
                                            numero_empleado=2132,nivel_escolar='Telesecundaria',profesion='Ama de casa',
                                            observaciones='Es a toda madre',idPersona=6,estatus=1)
                db.session.commit()

            # Commit any database changes; the User and Roles must exist before we can add a Role to the User
            
        except Exception as inst:
            message = {"result":"error"}
            logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
            return render_template('error.html')
    
    security = Security(app, userDataStore)
        
    try:
        
        # Initialize Flask-Admin
        admin = Admin(app)

        # Add Flask-Admin views for Users and Roles
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))
        
        
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
    
    @app.route('/login',methods=['GET','POST'])
    def index_login_fail():
   
        if request.method == 'POST' and request.form['email']:
            return render_template('security/login.html')
            print(request.form.get('next'))
        else:
            return render_template('security/login.html')
    try:
        #Registramos el blueprint para el resto de la aplicación
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        
        from .materialRutas import materialRutas as materialRutas_blueprint
        app.register_blueprint(materialRutas_blueprint)
        
        from .categoriasRutas import categoriasRutas as categoriasRutas_blueprint
        app.register_blueprint(categoriasRutas_blueprint)
        
        from .proveedorRutas import proveedorRutas as proveedorRutas_blueprint
        app.register_blueprint(proveedorRutas_blueprint)
        
        from .clienteRutas import clienteRutas as clienteRutas_blueprint
        app.register_blueprint(clienteRutas_blueprint)
        
        from .ventasRutas import ventasRutas as ventasRutas_blueprint
        app.register_blueprint(ventasRutas_blueprint)
        
        from .productoRutas import productoRutas as productoRutas_blueprint
        app.register_blueprint(productoRutas_blueprint)
        
        from .detalleProductoMaterialRutas import detalleProductoMaterialRutas as detalleProductoMaterialRutas_blueprint
        app.register_blueprint(detalleProductoMaterialRutas_blueprint)
        
        from .ordenCompraRutas import ordenCompraRutas as ordenCompraRutas_blueprint
        app.register_blueprint(ordenCompraRutas_blueprint)
        
        from .empleadoRutas import empleadoRutas as empleadoRutas_blueprint
        app.register_blueprint(empleadoRutas_blueprint)
        
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
    
    logging.info('Incio de la aplicacion ['+str(datetime.now())+']')
    
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    
    @app.errorhandler(404)
    def page_not_found(e):
        logging.error(str(type(e))+'\n Tipo de error: '+str(e)+ '['+str(datetime.now())+']')
        return render_template('error.html')
    
    @app.errorhandler(500)
    def page_not_found(e):
        logging.error(str(type(e))+'\n Tipo de error: '+str(e)+ '['+str(datetime.now())+']')
        return render_template('error.html')

