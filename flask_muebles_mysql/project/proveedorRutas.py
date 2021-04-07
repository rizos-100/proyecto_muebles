from flask import Blueprint, render_template, jsonify, request
from .models import db
from .models import proveedor,ProveedorSchema
import json

proveedorRutas = Blueprint('proveedorRutas', __name__)

@proveedorRutas.route('/getAllProveedor',methods=['GET','POST'])
def getAllProveedor():
    proveedores = db.session.query(proveedor).filter(proveedor.estatus == 'Activo').all()
    proveedor_schema =ProveedorSchema(many=True)
    result=proveedor_schema.dump(proveedores)
    return jsonify(result)

@proveedorRutas.route('/addProveedor',methods=['GET','POST'])
def addProveedor():
    if request.method=='POST':
        nombre_=request.form['nombre']
        rfc_=request.form['rfc']
        calle_=request.form['calle']
        colonia_=request.form['colonia']
        num_int=request.form['num_int']
        num_ext=request.form['num_ext']
        cp_=request.form['cp']
        nombreC=request.form['nombre_contacto']
        puestoC=request.form['puesto_contacto']
        telefonoC=request.form['telefono_contacto']
        correoC=request.form['correo_contacto']
        estatus_='Activo'
        estado_=request.form['estado']
        municipio_=request.form['municipio']
        
        prov=proveedor(nombre=nombre_,
                        rfc=rfc_,
                        calle=calle_,
                        colonia=colonia_,
                        numero_interior=num_int,
                        numero_exterior=num_ext,
                        cp=cp_,
                        nombre_contacto=nombreC,
                        puesto_contacto=puestoC,
                        telefono_contacto=telefonoC,
                        correo_contacto=correoC,
                        estatus=estatus_,
                        estado=estado_,
                        municipio=municipio_
                        )
        
        db.session.add(prov)
        db.session.commit()
        
        result = {"id":prov.id}
        
        return jsonify(result)

@proveedorRutas.route('/updateProveedor',methods=['GET','POST'])
def updateProveedor():
    if request.method == 'POST':
        id=request.form['id']
        nombre=request.form['nombre']
        rfc=request.form['rfc']
        calle=request.form['calle']
        colonia=request.form['colonia']
        num_int=request.form['num_int']
        num_ext=request.form['num_ext']
        cp=request.form['cp']
        nombreC=request.form['nombre_contacto']
        puestoC=request.form['puesto_contacto']
        telefonoC=request.form['telefono_contacto']
        correoC=request.form['correo_contacto']
        estado_=request.form['estado']
        municipio_=request.form['municipio']
        
        prov = db.session.query(proveedor).filter(proveedor.id==id).first()
        prov.nombre=nombre
        prov.rfc=rfc
        prov.calle=calle
        prov.colonia=colonia
        prov.numero_interior=num_int
        prov.numero_exterior=num_ext
        prov.cp=cp
        prov.nombre_contacto=nombreC
        prov.puesto_contacto=puestoC
        prov.telefono_contacto=telefonoC
        prov.correo_contacto=correoC
        prov.estado=estado_
        prov.municipio=municipio_
        
        db.session.commit()
        
        result={"id":prov.id}
        
        return jsonify(result)

@proveedorRutas.route('/deleteProveedor',methods=['POST','GET'])
def deleteProveedor():
    if request.method=='POST':
        id=request.form['id']
        prov=db.session.query(proveedor).filter(proveedor.id==id).first()
        prov.estatus='Inactivo'
        
        db.session.commit()
        
        result={"id":prov.id}
        
        return jsonify(result)
