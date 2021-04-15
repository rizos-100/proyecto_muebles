from flask import Blueprint, render_template, jsonify, request, make_response
from .models import ProveedorSchema, db, personaSchema
from .models import orden_compra,OrdenSchema,detalle_orden_compra,detalleOrdenSchema,proveedor,User,material,MaterialSchema,persona, domicilio
import json
#import datetime
from datetime import datetime
import logging
from project.validateInputs import validate as Validator

from flask_security import login_required
from flask_security.decorators import roles_accepted

ordenCompraRutas = Blueprint('ordenCompraRutas',__name__)


@ordenCompraRutas.route('/getAllOrdenCompra',methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllOrdenCompra():
    try:
        ordenes=db.session.query(orden_compra).all()
        arrayOrdenes = list()
        for orden in ordenes:
            provJson=ProveedorSchema(many=False)
            persJson=personaSchema(many=False)
            prov=db.session.query(proveedor).filter(proveedor.id==orden.proveedor).first()
            if prov:
                resProv=provJson.dump(prov)
            else:
                resProv={}
                
            us=db.session.query(User).filter(User.id==orden.user).first()
            if us:
                personUser = db.session.query(persona).filter(persona.id==us.idPersona).first()
                resUser=persJson.dump(personUser)
            else:
                resUser={}
            materia=db.session.query(detalle_orden_compra).filter(detalle_orden_compra.idOrden==orden.id).all()
            materiales=list()
            for det in materia:
                mat=db.session.query(material).filter(material.id==det.material).first()
                objM={
                    'id':det.id,
                    'cantidad':det.cantidad,
                    'subtotal':det.subtotal,
                    'idMaterial':det.material,
                    'material':mat.nombre, 
                    'tipo': mat.tipo
                }
                materiales.append(objM)
            #matSch=detalleOrdenSchema(many=True)
            #res=matSch.dump(materia)
            ordenObj={
            'id':orden.id,
            'proveedor':resProv,
            'usuario':resUser,
            'fecha_orden':orden.fecha_orden,
            'estatus':orden.estatus,
            'total':orden.total,
            'materiales':materiales
            }
            arrayOrdenes.append(ordenObj)
        #return jsonify(arrayOrdenes)
        return render_template("ordenCompra.html",ordenes=arrayOrdenes,activos=True)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template(message)
        #return render_template('error.html')


@ordenCompraRutas.route('/getAllOrdenCompraById',methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllOrdenCompraById():
    try:
        if request.method == 'POST':
            id = request.form['idOrden']
            orden=db.session.query(orden_compra).filter(orden_compra.id==id).first()
            provJson=ProveedorSchema(many=False)
            persJson=personaSchema(many=False)
            ordenJson=OrdenSchema(many=False)
            prov=db.session.query(proveedor).filter(proveedor.id==orden.proveedor).first()
            if prov:
                resProv=provJson.dump(prov)
            else:
                resProv={}
                
            us=db.session.query(User).filter(User.id==orden.user).first()
            if us:
                personUser = db.session.query(persona).filter(persona.id==us.idPersona).first()
                resUser=persJson.dump(personUser)
            else:
                resUser={}
            materia=db.session.query(detalle_orden_compra).filter(detalle_orden_compra.idOrden==orden.id).all()
            materiales=list()
            for det in materia:
                mat=db.session.query(material).filter(material.id==det.material).first()
                objM={
                    'id':det.id,
                    'cantidad':det.cantidad,
                    'subtotal':det.subtotal,
                    'idMaterial':det.material,
                    'material':mat.nombre,
                    'tipo': mat.tipo
                }
                materiales.append(objM)
            #matSch=detalleOrdenSchema(many=True)
            #res=matSch.dump(materia)
            ordenObj= ordenJson.dump(orden)
            ordenObj['user']=resUser
            ordenObj['proveedor']=resProv
            ordenObj['materiales']=materiales
        return jsonify(ordenObj)
        #return render_template("",orden=ordenObj,activos=True)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')


@ordenCompraRutas.route('/addOrdenCompra',methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def addOrdenCompra():
    try:
        if request.method=='POST':
            total_=Validator.validarDecimal(request.form['total'])
            proveedor_=int(request.form['idProveedor'])
            user_=int(request.form['idUser'])
            estatus_='Activa'
            now = datetime.now()
            fecha=now.strftime('%Y-%m-%d')
        
            orden=orden_compra(fecha_orden=fecha,
                            total=total_,
                            estatus=estatus_,
                            proveedor=proveedor_,
                            user=user_
            )
        
            db.session.add(orden)
            db.session.commit()
        
            materiales=json.loads(request.form['materiales_orden'])
            #print(materiales)
            for materia in materiales:
                idMaterial=materia['idMaterial']
                cant=int(materia['cantidad'])
                detalle=detalle_orden_compra(
                    cantidad=cant,
                    subtotal=Validator.validarDecimal(materia['subtotal']),
                    material=idMaterial,
                    idOrden=orden.id
                )
                db.session.add(detalle)
                db.session.commit()
                
                mat=db.session.query(material).filter(material.id==idMaterial).first()
                mat.cantidad=int(mat.cantidad)+int(cant)
                db.session.commit()
                
            result = {"id":orden.id}
            return jsonify(result)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)
        #return render_template(message)


@ordenCompraRutas.route('/getAllOrdenCompraByDia',methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllOrdenCompraByDia():
    try:
        materiales_lista = db.session.query(material).filter(material.estatus == "Disponible").all()
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
                'puesto_contacto':prov.puesto_contacto,
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
            
        now = datetime.now()
        fecha=now.strftime('%Y-%m-%d')
        #fecha='2021-04-07'
        ordenes=db.session.query(orden_compra).filter(orden_compra.fecha_orden==fecha).all()
        arrayOrdenes = list()
        for orden in ordenes:
            provJson=ProveedorSchema(many=False)
            persJson=personaSchema(many=False)
            prov=db.session.query(proveedor).filter(proveedor.id==orden.proveedor).first()
            if prov:
                resProv=provJson.dump(prov)
            else:
                resProv={}
                
            us=db.session.query(User).filter(User.id==orden.user).first()
            if us:
                personUser = db.session.query(persona).filter(persona.id==us.idPersona).first()
                resUser=persJson.dump(personUser)
            else:
                resUser={}
            materia=db.session.query(detalle_orden_compra).filter(detalle_orden_compra.idOrden==orden.id).all()
            materiales=list()
            for det in materia:
                mat=db.session.query(material).filter(material.id==det.material).first()
                objM={
                    'id':det.id,
                    'cantidad':det.cantidad,
                    'subtotal':det.subtotal,
                    'idMaterial':det.material,
                    'material':mat.nombre, 
                    'tipo': mat.tipo
                }
                materiales.append(objM)
            #matSch=detalleOrdenSchema(many=True)
            #res=matSch.dump(materia)
            ordenObj={
            'id':orden.id,
            'proveedor':resProv,
            'usuario':resUser,
            'fecha_orden':orden.fecha_orden,
            'estatus':orden.estatus,
            'total':orden.total,
            'materiales':materiales
            }
            arrayOrdenes.append(ordenObj)
        #return jsonify(arrayOrdenes)
        return render_template("ordenCompraDia.html",ordenes=arrayOrdenes,activos=True, proveedores=arrayProveedores, materiales=materiales_lista)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
        #return render_template(message)


@ordenCompraRutas.route('/getMateriaOrdenById',methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def getMateriaOrdenById():
     if request.method == 'GET':
          idM = request.args.get("id", "No contiene el nombre")
          material_ = db.session.query(material).filter(material.id == idM, material.estatus == "Disponible").first()
          material_schema = MaterialSchema(many=False)
          result = material_schema.dump(material_)
          return jsonify(result)