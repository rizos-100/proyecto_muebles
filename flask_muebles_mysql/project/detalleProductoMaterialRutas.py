from flask import Blueprint, render_template, jsonify, request
from .models import db, detalle_producto_material, producto, material, Detalle_produco_material_Schema
import logging
from datetime import datetime
from project.validateInputs import validate as Validator

from flask_security import login_required
from flask_security.decorators import  roles_accepted

detalleProductoMaterialRutas = Blueprint('detalleProductoMaterialRutas', __name__)

@detalleProductoMaterialRutas.route('/getAllDetalleProductosMaterial', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllDetalleProductosMaterial():
    if request.method == 'GET':
        try:
            idProducto_ = request.args.get("idProducto", "No contiene el nombre")
            dtmp = db.session.query(detalle_producto_material, material).join(detalle_producto_material.material).filter(detalle_producto_material.idProducto == idProducto_).all()
          
            arrayDPM = list()
            for i in dtmp:
                dtmpObj ={
                    'id': i.detalle_producto_material.id,
                    'alto': i.detalle_producto_material.alto,
                    'ancho': i.detalle_producto_material.ancho,
                    'cantidad': i.detalle_producto_material.cantidad,
                    'material':{
                        'idMaterial':i.material.id,
                        'nombre':i.material.nombre,
                        'tipo': i.material.tipo,
                        'descripcion':i.material.descripcion,
                        'cantidad': i.material.cantidad,
                        'alto': i.material.alto,
                        'ancho': i.material.ancho,
                        'grosor': i.material.grosor,
                        'color': i.material.color,
                        'estatus':i.material.estatus,
                        }
                    }
                arrayDPM.append(dtmpObj) 
            return render_template("", dtmp = arrayDPM)
        except Exception as inst:
            message = {"result":"error"}
            logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
            return render_template('error.html')
          


@detalleProductoMaterialRutas.route('/addDetalleProductosMaterial', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def addDetalleProductosMaterial():
    if request.method == 'POST':
        try:
            alto_ = Validator.validarDecimal(request.form['alto'])
            ancho_ = Validator.validarDecimal(request.form['ancho'])
            cantidad_ = Validator.validarDecimal(request.form['cantidad'])
            idProducto_ = request.form['idProducto']
            idMaterial_ = request.form['idMaterial']
          
          
            dpm = detalle_producto_material(alto = alto_,
                                            ancho = ancho_,
                                            cantidad = cantidad_,
                                            idProducto = idProducto_,
                                            idMaterial = idMaterial_)
            
            db.session.add(dpm)
            db.session.commit()
            
            result = {"id": dpm.id}
            
            return jsonify(result)
        except Exception as inst:
            message = {"result":"error"}
            logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
            return render_template('error.html')
        