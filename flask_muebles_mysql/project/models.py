#from . import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_security import UserMixin, RoleMixin, current_user, utils
from flask_admin import Admin
from flask_admin.contrib  import sqla
import datetime
from wtforms.fields import PasswordField

db = SQLAlchemy()
ma = Marshmallow()

#Definiendo la tabla relacional
users_roles = db.Table('users_roles',
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('roleId', db.Integer, db.ForeignKey('role.id')))

class persona (db.Model):
    __tablename__='persona'
    id=db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellidoP = db.Column(db.String(255), nullable=False)
    apellidoM = db.Column(db.String(255), nullable=False)
    numero_fijo = db.Column(db.String(10), nullable=False)
    celular = db.Column(db.String(10), nullable=False)
    estatus = db.Column(db.String(100), nullable=False)
    domicilio = db.Column(db.Integer,db.ForeignKey('domicilio.id'))
    rfc = db.Column(db.String(255), nullable=False)

    domicil = db.relationship('domicilio')

class User(UserMixin, db.Model):
    """User account model"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    numero_empleado = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    nivel_escolar = db.Column(db.String(255), nullable=False)
    profesion = db.Column(db.String(255), nullable=False)
    observaciones = db.Column(db.String(255), nullable=True)
    idPersona = db.Column(db.Integer,db.ForeignKey('persona.id'))
    estatus = db.Column(db.Boolean)
    confirmed_at = db.Column(db.Date,default=datetime.datetime.now)
    roles = db.relationship('Role',
        secondary=users_roles,
        backref= db.backref('users', lazy='dynamic'))
    
class Role(RoleMixin, db.Model):
    """Role model"""

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description =  db.Column(db.String(255))
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

class proveedor(db.Model):
    __tablename__='proveedor'
    id=db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    rfc = db.Column(db.String(255), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    colonia = db.Column(db.String(255), nullable=False)
    numero_interior = db.Column(db.String(10), nullable=True)
    numero_exterior = db.Column(db.String(10), nullable=True)
    cp = db.Column(db.String(10), nullable=True)
    nombre_contacto = db.Column(db.String(255), nullable=False)
    puesto_contacto = db.Column(db.String(255), nullable=False)
    telefono_contacto = db.Column(db.String(10), nullable=False)
    correo_contacto = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    municipio = db.Column(db.String(255), nullable=False)

class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre','rfc','calle','colonia','numero_interior','numero_exterior','cp',
                    'nombre_contacto','puesto_contacto','telefono_contacto','correo_contacto','estatus',
                    'estado','municipio')
    

class domicilio (db.Model):
    __tablename__='domicilio'
    id=db.Column(db.Integer,primary_key=True)
    calle = db.Column(db.String(255), nullable=False)
    colonia = db.Column(db.String(255), nullable=False)
    numero_interior = db.Column(db.String(10), nullable=True)
    numero_exterior = db.Column(db.String(10), nullable=True)
    estado = db.Column(db.String(255), nullable=False)
    municipio = db.Column(db.String(255), nullable=False)
    cp = db.Column(db.String(10), nullable=True)
    referencias = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(100), nullable=False)

class cliente (db.Model):
    __tablename__='cliente'
    id=db.Column(db.Integer,primary_key=True)
    idPersona = db.Column(db.Integer,db.ForeignKey('persona.id'))
    
    persona = db.relationship('persona')



class orden_compra (db.Model):
    __tablename__='orden_compra'
    id=db.Column(db.Integer,primary_key=True)
    fecha_orden = db.Column(db.Date,default=datetime.datetime.now)
    total=db.Column(db.Float,nullable=False)
    estatus = db.Column(db.String(100), nullable=False)
    proveedor = db.Column(db.Integer,db.ForeignKey('proveedor.id'))
    user = db.Column(db.Integer,db.ForeignKey('user.id'))

class material(db.Model):
    __tablename__='material'
    id=db.Column(db.Integer,primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer,nullable=False)
    alto = db.Column(db.Integer,nullable=False)
    ancho = db.Column(db.Integer,nullable=False)
    grosor = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(100), nullable=False)
    estatus = db.Column(db.String(100), nullable=False)
    
class MaterialSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tipo', 'nombre', 'descripcion', 'cantidad', 'alto', 'ancho', 'grosor', 'color', 'estatus')


class detalle_orden_compra (db.Model):
    __tablename__='detalle_orden_compra'
    id=db.Column(db.Integer,primary_key=True)
    cantidad=db.Column(db.Integer,nullable=False)
    subtotal=db.Column(db.Float,nullable=False)
    material = db.Column(db.Integer,db.ForeignKey('material.id'))

class sobrante_material (db.Model):
    __tablename__='sobrante_material'
    id=db.Column(db.Integer,primary_key=True)
    alto = db.Column(db.Integer,nullable=False)
    ancho = db.Column(db.Integer,nullable=False)
    comentario = db.Column(db.String(255), nullable=True)
    estatus = db.Column(db.String(100), nullable=False)
    material = db.Column(db.Integer,db.ForeignKey('material.id'))
    
class SobranteMaterialSchema(ma.Schema):
    class Meta:
        fields = ('id', 'alto', 'ancho', 'comentario', 'estatus', 'material')



class categoria (db.Model):
    __tablename__='categoria'
    id=db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(100), nullable=False)
    
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'estatus')

class producto (db.Model):
    __tablename__='producto'
    id=db.Column(db.Integer,primary_key=True)
    modelo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    img = db.Column(db.Text, nullable=False)
    peso = db.Column(db.Float,nullable=False)
    color = db.Column(db.String(100), nullable=False)
    alto = db.Column(db.Float,nullable=False)
    ancho = db.Column(db.Float,nullable=False)
    largo = db.Column(db.Float,nullable=False)
    cantidad = db.Column(db.Integer,nullable=False)
    cantidad_minima = db.Column(db.Integer,nullable=False)
    precio = db.Column(db.Float,nullable=False)
    estatus = db.Column(db.String(100), nullable=False)
    idCategoria = db.Column(db.Integer,db.ForeignKey('categoria.id'))
    
    categoria = db.relationship('categoria')
    
    
class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id','modelo','descripcion','img','peso','color','alto','ancho','largo','cantidad','cantidad_minima','precio', 'estatus', 'categoria')

class detalle_producto_material (db.Model):
    __tablename__='detalle_producto_material'
    id=db.Column(db.Integer,primary_key=True)
    alto = db.Column(db.Float,nullable=False)
    ancho = db.Column(db.Float,nullable=False)
    cantidad = db.Column(db.Integer,nullable=False)
    producto = db.Column(db.Integer,db.ForeignKey('producto.id'))
    material = db.Column(db.Integer,db.ForeignKey('material.id'))

class Detalle_produco_material_Schema(ma.Schema):
    class Meta:
        fields = ('id','alto','ancho','cantidad','producto','material')

class venta (db.Model):
    __tablename__='venta'
    id=db.Column(db.Integer,primary_key=True)
    fecha_venta = db.Column(db.Date,default=datetime.datetime.now)
    total = db.Column(db.Float,nullable=False)
    cliente = db.Column(db.Integer,db.ForeignKey('cliente.id'))
    user = db.Column(db.Integer,db.ForeignKey('user.id'))

class detalle_venta (db.Model):
    __tablename__='detalle_venta'
    id=db.Column(db.Integer,primary_key=True)
    cantidad = db.Column(db.Integer,nullable=False)
    subtotal = db.Column(db.Float,nullable=False)
    venta = db.Column(db.Integer,db.ForeignKey('venta.id'))
    producto = db.Column(db.Integer,db.ForeignKey('producto.id'))