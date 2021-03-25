import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, utils, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib  import sqla
from wtforms.fields import PasswordField

#Creamos una instancia de SQLAlchemy
db = SQLAlchemy()
#Creamos el objeto SQLalchemyUserDaaStore
from .models import User, Role, RoleAdmin, UserAdmin

userDataStore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
    #Creamos una instancia del flask
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generar la clave de sessión para crear una cookie con la inf. de la sessión
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flasksecurity'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()

        #Conectando los modelos a flask-security.
        security = Security(app, userDataStore)

        ######################################################################
        userDataStore.find_or_create_role(name='admin', description='Administrator')
        userDataStore.find_or_create_role(name='end-user', description='End user')

        if not userDataStore.get_user('enduser@example.com'):
            userDataStore.create_user(name ='User-End',email='enduser@example.com', password=generate_password_hash('password', method='sha256'))
        if not userDataStore.get_user('admin@example.com'):
            userDataStore.create_user(name= 'Admin', email='admin@example.com', password=generate_password_hash('password', method='sha256'))

        db.session.commit()

        userDataStore.add_role_to_user('enduser@example.com', 'end-user')
        userDataStore.add_role_to_user('admin@example.com', 'admin')
        db.session.commit()
    
    #####################################################################3
    #Configurando el login_manager
    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    #Importamos la clase User.
    #from .models import User
    #@login_manager.user_loader
    #def load_user(user_id):
        #return User.query.get(int(user_id))

    #Registramos el blueprint para las rutas auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Registramos el blueprint para el resto de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Initialize Flask-Admin
    admin = Admin(app)

    # Add Flask-Admin views for Users and Roles
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    
    return app

