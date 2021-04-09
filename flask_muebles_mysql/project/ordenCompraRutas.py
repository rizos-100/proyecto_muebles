from flask import Blueprint, render_template, jsonify, request, make_response
from .models import db
from .models import orden_compra,OrdenSchema,detalle_orden_compra,detalleOrdenSchema,proveedor,User,material,MaterialSchema
import json
#import datetime
from datetime import datetime
import logging

ordenCompraRutas = Blueprint('ordenCompraRutas',__name__)

#@login_required
#@roles_accepted('admin','almacenista')
@ordenCompraRutas.route('/getAllOrdenCompra',methods=['GET','POST'])
def getAllOrdenCompra():
    try:
        ordenes=db.session.query(orden_compra).all()
        arrayOrdenes = list()
        for orden in ordenes:
            prov=db.session.query(proveedor).filter(proveedor.id==orden.proveedor).first()
            us=db.session.query(User).filter(User.id==orden.user).first()
            materia=db.session.query(detalle_orden_compra).filter(detalle_orden_compra.idOrden==orden.id).all()
            materiales=list()
            for det in materia:
                mat=db.session.query(material).filter(material.id==det.material).first()
                objM={
                    'id':det.id,
                    'cantidad':det.cantidad,
                    'subtotal':det.subtotal,
                    'idMaterial':det.material,
                    'material':mat.nombre
                }
                materiales.append(objM)
            #matSch=detalleOrdenSchema(many=True)
            #res=matSch.dump(materia)
            ordenObj={
            'id':orden.id,
            'idProveedor':prov.id,
            'proveedor':prov.nombre,
            'idUsuario':us.id,
            'usuario':us.correo,
            'fecha_orden':orden.fecha_orden,
            'estatus':orden.estatus,
            'total':orden.total,
            'materiales':materiales
            }
            arrayOrdenes.append(ordenObj)
        #return jsonify(arrayOrdenes)
        return render_template("",ordenes=arrayOrdenes,activos=True)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

#@login_required
#@roles_accepted('admin','almacenista')
@ordenCompraRutas.route('/addOrdenCompra',methods=['GET','POST'])
def addOrdenCompra():
    try:
        if request.method=='POST':
            total_=float(request.form['total'])
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
        
            materiales=json.loads(request.form['materiales'])
            #print(materiales)
            for materia in materiales:
                idMaterial=materia['idMaterial']
                cant=materia['cantidad']
                detalle=detalle_orden_compra(
                    cantidad=cant,
                    subtotal=materia['subtotal'],
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


####################  ESTE APARTADO DE UPDATE NO ESTA TERMINADO AUN ################################3
#@login_required
#@roles_accepted('admin','almacenista')
@ordenCompraRutas.route('/updateOrdenCompra',methods=['GET','POST'])
def updateOrdenCompra():
    try:
        if request.method=='POST':
            id=int(request.form['id'])
            total_=float(request.form['total'])
            proveedor_=int(request.form['idProveedor'])
            user_=int(request.form['idUser'])
            fecha_=request.form['fecha']
            orden=db.session.query(orden_compra).filter(orden_compra.id==id).first()
            orden.total=total_
            orden.proveedor=proveedor_
            orden.user=user_
            orden.fecha_orden=fecha_
            db.session.commit()
        
            materiales=json.loads(request.form['materiales'])
            #print(materiales)
            for materia in materiales:
                idM=int(materia['id'])
                cantidad=materia['cantidad']
                subtotal=materia['subtotal']
                material=materia['idMaterial']
                detalle=db.session.query(detalle_orden_compra).filter(detalle_orden_compra.id==idM).first()
                detalle.cantidad=cantidad
                detalle.subtotal=subtotal
                detalle.material=material
                db.session.commit()
            result = {"id":orden.id}
            return jsonify(result)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        #return message
        return make_response(jsonify(message), 400)