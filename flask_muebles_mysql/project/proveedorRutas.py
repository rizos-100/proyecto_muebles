from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db
from .models import proveedor,ProveedorSchema,domicilio,DomicilioSchema
import json
from .validateInputs import validate
import logging
from datetime import datetime
proveedorRutas = Blueprint('proveedorRutas', __name__)

#@login_required
#@roles_accepted('admin','almacenista','vendedor')
@proveedorRutas.route('/getAllProveedorActivos',methods=['GET','POST'])
def getAllProveedor():
    try:
        proveedores = db.session.query(proveedor).filter(proveedor.estatus == 'Activo').all()
        arrayProveedores=list()
        for prov in proveedores:
            dom=db.session.query(domicilio).filter(domicilio.id==prov.idDomicilio).first()
            #domSch=DomicilioSchema(many=True)
            #domic=domSch.dump(dom)
            provObj={
                'id':prov.id,
                'nombre':prov.nombre,
                'rfc':prov.rfc,
                'nombre_contacto':prov.nombre_contacto,
                'puesto_contacto':prov.nombre_contacto,
                'telefono_contacto':prov.telefono_contacto,
                'correo_contacto':prov.correo_contacto,
                'estatus':prov.estatus,
                'domicilio':{
                    'calle':dom.calle,
                    'num_ext':dom.numero_exterior,
                    'num_int':dom.numero_interior,
                    'colonia':dom.colonia,
                    'municipio':dom.municipio,
                    'estado':dom.estado,
                    'cp':dom.cp,
                    'referencias':dom.referencias
                }
            }
            arrayProveedores.append(provObj)
        #return jsonify(arrayProveedores)
        render_template("",proveedores=arrayProveedores,activos=True)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
    
#@login_required
#@roles_accepted('admin','almacenista','vendedor')
@proveedorRutas.route('/getAllProveedorInactivos',methods=['GET','POST'])
def getAllProveedorIn():
    try:
        proveedores = db.session.query(proveedor).filter(proveedor.estatus == 'Inactivo').all()
        arrayProveedores=list()
        for prov in proveedores:
            dom=db.session.query(domicilio).filter(domicilio.id==prov.idDomicilio).first()
            #domSch=DomicilioSchema(many=True)
            #domic=domSch.dump(dom)
            provObj={
                'id':prov.id,
                'nombre':prov.nombre,
                'rfc':prov.rfc,
                'nombre_contacto':prov.nombre_contacto,
                'puesto_contacto':prov.nombre_contacto,
                'telefono_contacto':prov.telefono_contacto,
                'correo_contacto':prov.correo_contacto,
                'estatus':prov.estatus,
                'domicilio':{
                    'calle':dom.calle,
                    'num_ext':dom.numero_exterior,
                    'num_int':dom.numero_interior,
                    'colonia':dom.colonia,
                    'municipio':dom.municipio,
                    'estado':dom.estado,
                    'cp':dom.cp,
                    'referencias':dom.referencias
                }
            }
            arrayProveedores.append(provObj)
        #return jsonify(arrayProveedores)
        render_template("",proveedores=arrayProveedores,activos=False)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

#@login_required
#@roles_accepted('admin','almacenista')
@proveedorRutas.route('/addProveedor',methods=['GET','POST'])
def addProveedor():
    try:
        if request.method=='POST':
            nombre_=validate.sanitizarNombre(request.form['nombre'])
            rfc_=validate.validarRFC(request.form['rfc'])
            calle_=validate.sanitizarNombre(request.form['calle'])
            colonia_=validate.sanitizarNombre(request.form['colonia'])
            num_int=request.form['num_int']
            num_ext=request.form['num_ext']
            cp_=request.form['cp']
            nombreC=validate.sanitizarNombre(request.form['nombre_contacto'])
            puestoC=validate.sanitizarNombre(request.form['puesto_contacto'])
            telefonoC=request.form['telefono_contacto']
            correoC=validate.sanitizarCorreo(request.form['correo_contacto'])
            estatus_='Activo'
            estado_=validate.sanitizarNombre(request.form['estado'])
            municipio_=validate.sanitizarNombre(request.form['municipio'])
            referencias_=validate.sanitizarNombre(request.form['referencias'])
        
            dom=domicilio(
                calle=calle_,
                colonia=colonia_,
                numero_interior=num_int,
                numero_exterior=num_ext,
                estado=estado_,
                municipio=municipio_,
                cp=cp_,
                referencias=referencias_,
                estatus=estatus_
            
            )
            db.session.add(dom)
            db.session.commit()
        
            prov=proveedor(nombre=nombre_,
                        rfc=rfc_,
                        nombre_contacto=nombreC,
                        puesto_contacto=puestoC,
                        telefono_contacto=telefonoC,
                        correo_contacto=correoC,
                        estatus=estatus_,
                        idDomicilio=dom.id
                        )
        
            db.session.add(prov)
            db.session.commit()
        
            result = {"id":prov.id}
        
            return jsonify(result)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)

#@login_required
#@roles_accepted('admin','almacenista')
@proveedorRutas.route('/updateProveedor',methods=['GET','POST'])
def updateProveedor():
    try:
        if request.method == 'POST':
            id=request.form['id']
            idDomicilio=request.form['idDomicilio']
            nombre_=validate.sanitizarNombre(request.form['nombre'])
            rfc_=validate.validarRFC(request.form['rfc'])
            calle_=validate.sanitizarNombre(request.form['calle'])
            colonia_=validate.sanitizarNombre(request.form['colonia'])
            cp_=request.form['cp']
            nombreC=validate.sanitizarNombre(request.form['nombre_contacto'])
            puestoC=validate.sanitizarNombre(request.form['puesto_contacto'])
            telefonoC=request.form['telefono_contacto']
            correoC=validate.sanitizarCorreo(request.form['correo_contacto'])
            estado_=validate.sanitizarNombre(request.form['estado'])
            municipio_=validate.sanitizarNombre(request.form['municipio'])
            referencias_=validate.sanitizarNombre(request.form['referencias'])
            num_int=request.form['num_int']
            num_ext=request.form['num_ext']

        
            prov = db.session.query(proveedor).filter(proveedor.id==id).first()
            prov.nombre=nombre_
            prov.rfc=rfc_
            prov.nombre_contacto=nombreC
            prov.puesto_contacto=puestoC
            prov.telefono_contacto=telefonoC
            prov.correo_contacto=correoC
            db.session.commit()
        
            dom=db.session.query(domicilio).filter(domicilio.id==idDomicilio).first()
            dom.calle=calle_
            dom.colonia=colonia_
            dom.cp=cp_
            dom.estado=estado_
            dom.municipio=municipio_
            dom.numero_exterior=num_ext
            dom.numero_interior=num_int
            dom.referencias=referencias_
            db.session.commit()
        
            result={"id":prov.id}
        
            return jsonify(result)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)

#@login_required
#@roles_accepted('admin','almacenista')
@proveedorRutas.route('/deleteProveedor',methods=['POST','GET'])
def deleteProveedor():
    try:
        if request.method=='POST':
            id=request.form['id']
            prov=db.session.query(proveedor).filter(proveedor.id==id).first()
            prov.estatus='Inactivo'
        
            db.session.commit()
        
            result={"id":prov.id}
        
            return jsonify(result)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)


#@login_required
#@roles_accepted('admin','almacenista')
@proveedorRutas.route('/getAllProveedorById',methods=['GET','POST'])
def getAllProveedorbyId():
    try:
        if request.method == 'POST':
            id = request.form['idProveedor']
            prov = db.session.query(proveedor).filter(proveedor.id == id).first()
            dom=db.session.query(domicilio).filter(domicilio.id==prov.idDomicilio).first()
            #domSch=DomicilioSchema(many=True)
            #domic=domSch.dump(dom)
            provObj={
                'id':prov.id,
                'nombre':prov.nombre,
                'rfc':prov.rfc,
                'nombre_contacto':prov.nombre_contacto,
                'puesto_contacto':prov.nombre_contacto,
                'telefono_contacto':prov.telefono_contacto,
                'correo_contacto':prov.correo_contacto,
                'estatus':prov.estatus,
                'domicilio':{
                    'calle':dom.calle,
                    'num_ext':dom.numero_exterior,
                    'num_int':dom.numero_interior,
                    'colonia':dom.colonia,
                    'municipio':dom.municipio,
                    'estado':dom.estado,
                    'cp':dom.cp,
                    'referencias':dom.referencias
                }
            }
        #return jsonify(provObj)
        render_template("",proveedor=provObj,activos=True)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
    