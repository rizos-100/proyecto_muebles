from flask import Blueprint, render_template,request
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from . import db
from .models import material, venta, MaterialSchema, sobrante_material, SobranteMaterialSchema,producto,detalle_producto_material as dpm,material
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
@main.route('/tablero')
@login_required
@roles_accepted('admin','vendedor','almacenista')#autorización para el rol admin
def index_login():
    try:
        arrayRecom = list()
        arrayRecList = list()
        productos = db.session.query(producto).filter(producto.estatus == 'Activo').all()
        
        for i in productos:
            if i.cantidad < i.cantidad_minima:
                detalle_mate = db.session.query(dpm,material).join(dpm.material).filter(dpm.idProducto == i.id).all()
                for j in detalle_mate:
                        objRec = {
                        "idMaterial":j.material.id,
                        "nombre":j.material.nombre,
                        "tipo":j.material.tipo,
                        "cantidadRecom":j.detalle_producto_material.cantidad * (i.cantidad_minima - i.cantidad)  
                        }
                        arrayRecom.append(objRec)
            
        materiales = db.session.query(material).filter(material.estatus == 'Disponible').all()
        for k in materiales:
            cont = 0
            for l in arrayRecom:
                if k.id == l['idMaterial'] and int(l['cantidadRecom']) > 0:
                        print(l)
                        cont = int(l['cantidadRecom']) + cont
            if cont > 0:
                objRec = {
                            "idMaterial":k.id,
                            "nombre":k.nombre,
                            "tipo":k.tipo,
                            "cantidadRecom": cont
                        }     
                arrayRecList.append(objRec)
            cont = 0

        now = datetime.now()
        fechaHoy = now.strftime('%Y-%m-%d')
        ventas = db.session.query(venta).filter(venta.fecha_venta==fechaHoy, venta.estatus=='Activo').all()
        numVen = 0
        for i in ventas:
            numVen = numVen + 1
        return render_template('index.html', user=current_user, materiales=arrayRecList, ventas = numVen)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

