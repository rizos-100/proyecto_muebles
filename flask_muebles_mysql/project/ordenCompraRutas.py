from flask import Blueprint, render_template, jsonify, request
from .models import db
from .models import orden_compra,OrdenSchema,detalle_orden_compra,detalleOrdenSchema,proveedor,User
import json
#import datetime
from datetime import datetime

ordenCompraRutas = Blueprint('ordenCompraRutas',__name__)

#@login_required
#@roles_accepted('admin','almacenista')
@ordenCompraRutas.route('/getAllOrdenCompra',methods=['GET','POST'])
def getAllOrdenCompra():
    ordenes=db.session.query(orden_compra).all()
    arrayOrdenes = list()
    for orden in ordenes:
        prov=db.session.query(proveedor).filter(proveedor.id==orden.proveedor).first()
        us=db.session.query(User).filter(User.id==orden.user).first()
        materia=db.session.query(detalle_orden_compra).filter(detalle_orden_compra.idOrden==orden.id).all()
        matSch=detalleOrdenSchema(many=True)
        res=matSch.dump(materia)
        ordenObj={
            'id':orden.id,
            'proveedor':prov.nombre,
            'usuario':us.correo,
            'fecha_orden':orden.fecha_orden,
            'estatus':orden.estatus,
            'total':orden.total,
            'materiales':res
        }
        arrayOrdenes.append(ordenObj)
    return jsonify(arrayOrdenes)

#@login_required
#@roles_accepted('admin','almacenista')
@ordenCompraRutas.route('/addOrdenCompra',methods=['GET','POST'])
def addOrdenCompra():
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
        print(materiales)
        for materia in materiales:
            detalle=detalle_orden_compra(
                cantidad=materia['cantidad'],
                subtotal=materia['subtotal'],
                material=materia['idMaterial'],
                idOrden=orden.id
            )
            db.session.add(detalle)
            db.session.commit()
        result = {"id":orden.id}
        return jsonify(result)

#@login_required
#@roles_accepted('admin','almacenista')
@ordenCompraRutas.route('/updateOrdenCompra',methods=['GET','POST'])
def updateOrdenCompra():
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
            