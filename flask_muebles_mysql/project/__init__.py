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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u512768467_user_produccio:7=Vhafn^K9@31.170.161.1/u512768467_muebleria'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()

        #Conectando los modelos a flask-security.
        security = Security(app, userDataStore)
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
    
    from .materialRutas import materialRutas as materialRutas_blueprint
    app.register_blueprint(materialRutas_blueprint)
    
    from .categoriasRutas import categoriasRutas as categoriasRutas_blueprint
    app.register_blueprint(categoriasRutas_blueprint)
    from .proveedorRutas import proveedorRutas as proveedorRutas_blueprint
    app.register_blueprint(proveedorRutas_blueprint)
    from .clienteRutas import clienteRutas as clienteRutas_blueprint
    app.register_blueprint(clienteRutas_blueprint)
        
    # Initialize Flask-Admin
    admin = Admin(app)

    # Add Flask-Admin views for Users and Roles
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    
    return app

