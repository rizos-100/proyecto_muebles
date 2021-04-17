from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db
from .models import cliente,persona,personaSchema,User,venta,VentaSchema,detalle_venta,Detalle_ventaSchema,producto,ProductoSchema,ClienteSchema, domicilio, categoria
import json
from project.validateInputs import validate as Validator
import logging
from datetime import datetime

from flask_security import login_required
from flask_security.decorators import roles_accepted


ventasRutas = Blueprint('ventasRutas', __name__)

@ventasRutas.route('/getAllVentasActivas',methods=['GET','POST'])
@login_required
@roles_accepted('admin','vendedor')
def getAllVentas():
    try:
        ventasArray = list()
        ventas = db.session.query(venta).filter(venta.estatus=='Activo').all()
        
        for i in ventas:
            persJson=personaSchema(many=False)
            produJson=ProductoSchema(many=False)
            detVenJson=Detalle_ventaSchema(many=False)
            ventJson=VentaSchema(many=False)
            clienJson=ClienteSchema(many=False)
            
            clientePers = db.session.query(cliente).filter(cliente.id==i.cliente).first()
            if clientePers:
                resCliente=clienJson.dump(clientePers)
                clientePers = db.session.query(persona).filter(persona.id==clientePers.idPersona).first()
                resCliente['idPersona'] = persJson.dump(clientePers)
            else:
                resCliente={}
                
            userSea = db.session.query(User).filter(User.id==i.user).first()
            if userSea:
                personUser = db.session.query(persona).filter(persona.id==userSea.idPersona).first()
                resUser=persJson.dump(personUser)
            else:
                resUser={}
            
            detalleVent = db.session.query(detalle_venta,producto).join(
                            detalle_venta.productoForegin).filter(detalle_venta.venta==i.id).all()
            detalleVentaArray = list()
            for j in detalleVent:
                objDetalle = detVenJson.dump(j.detalle_venta)
                objDetalle['producto']=produJson.dump(j.producto)
                
                detalleVentaArray.append(objDetalle)
            
            objVenta= ventJson.dump(i)
            objVenta['user']=resUser
            objVenta['cliente']=resCliente
            objVenta['detalleVenta']=detalleVentaArray

            ventasArray.append(objVenta)        

        return render_template('venta.html', ventas=ventasArray, activos = True)
        #return make_response(jsonify(ventasArray), 200)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@ventasRutas.route('/getAllVentasInactivas',methods=['GET','POST'])
@login_required
@roles_accepted('admin','vendedor')
def getAllVentasInactivas():
    try:
        ventasArray = list()
        ventas = db.session.query(venta).filter(venta.estatus=='Inactivo').all()
        
        for i in ventas:
            persJson=personaSchema(many=False)
            produJson=ProductoSchema(many=False)
            detVenJson=Detalle_ventaSchema(many=False)
            ventJson=VentaSchema(many=False)
            clienJson=ClienteSchema(many=False)
            
            clientePers = db.session.query(cliente).filter(cliente.id==i.cliente).first()
            if clientePers:
                resCliente=clienJson.dump(clientePers)
                clientePers = db.session.query(persona).filter(persona.id==clientePers.idPersona).first()
                resCliente['idPersona'] = persJson.dump(clientePers)
            else:
                resCliente={}
                
            userSea = db.session.query(User).filter(User.id==i.user).first()
            if userSea:
                personUser = db.session.query(persona).filter(persona.id==userSea.idPersona).first()
                resUser=persJson.dump(personUser)
            else:
                resUser={}
            
            detalleVent = db.session.query(detalle_venta,producto).join(
                            detalle_venta.productoForegin).filter(detalle_venta.venta==i.id).all()
            detalleVentaArray = list()
            for j in detalleVent:
                objDetalle = detVenJson.dump(j.detalle_venta)
                objDetalle['producto']=produJson.dump(j.producto)
                
                detalleVentaArray.append(objDetalle)
            
            objVenta= ventJson.dump(i)
            objVenta['user']=resUser
            objVenta['cliente']=resCliente
            objVenta['detalleVenta']=detalleVentaArray

            ventasArray.append(objVenta)        

        return render_template('venta.html', ventas=ventasArray, activos = False)
        #return make_response(jsonify(ventasArray), 200)
    
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@ventasRutas.route('/getAllVentasById',methods=['GET','POST'])
@login_required
@roles_accepted('admin','vendedor')
def getAllVentasById():
    try:

        if request.method == 'GET':
            
            idVent = int(request.args.get('idVenta','0'))
            ventasArray = list()
            ventas = db.session.query(venta).filter(venta.id==idVent).all()
            
            for i in ventas:
                persJson=personaSchema(many=False)
                produJson=ProductoSchema(many=False)
                detVenJson=Detalle_ventaSchema(many=False)
                ventJson=VentaSchema(many=False)
                clienJson=ClienteSchema(many=False)
                
                clientePers = db.session.query(cliente).filter(cliente.id==i.cliente).first()
                if clientePers:
                    resCliente=clienJson.dump(clientePers)
                    clientePers = db.session.query(persona).filter(persona.id==clientePers.idPersona).first()
                    resCliente['idPersona'] = persJson.dump(clientePers)
                else:
                    resCliente={}
                    
                userSea = db.session.query(User).filter(User.id==i.user).first()
                if userSea:
                    personUser = db.session.query(persona).filter(persona.id==userSea.idPersona).first()
                    resUser=persJson.dump(personUser)
                else:
                    resUser={}
                
                detalleVent = db.session.query(detalle_venta,producto).join(
                                detalle_venta.productoForegin).filter(detalle_venta.venta==i.id).all()
                detalleVentaArray = list()
                for j in detalleVent:
                    objDetalle = detVenJson.dump(j.detalle_venta)
                    objDetalle['producto']=produJson.dump(j.producto)
                    
                    detalleVentaArray.append(objDetalle)
                
                objVenta= ventJson.dump(i)
                objVenta['user']=resUser
                objVenta['cliente']=resCliente
                objVenta['detalleVenta']=detalleVentaArray

                ventasArray.append(objVenta)        

            #return render_template('', ventas=ventasArray)
            return jsonify(ventasArray)

    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
    
@ventasRutas.route('/addVenta',methods=['GET','POST'])
@login_required
@roles_accepted('admin','vendedor')
def addVenta():
    try:
        if request.method == 'POST':
            now = datetime.now()
            fechaVent_ = now.strftime('%Y-%m-%d')
            total_ = int(request.form['total'])
            idCli_ = int(request.form['cliente'])
            idUse_ = int(request.form['user'])
            
            objVent = venta(fecha_venta=fechaVent_,
                            total=total_,
                            cliente=idCli_,
                            user=idUse_,
                            estatus='Activo')
            
            db.session.add(objVent)
            db.session.commit()
            db.session.refresh(objVent)
            #print(objVent.id)
            detalleVen = json.loads(request.form['detalleVenta'])
            #print(objVent.id)
            for i in detalleVen:
                idProd = int(i['producto'])
                producto_upd = db.session.query(producto).filter(producto.id == idProd).first()
                producto_upd.cantidad = producto_upd.cantidad - int(i['cantidad'])
                
                db.session.commit()
                
                objDetalleVen = detalle_venta(cantidad=int(i['cantidad']),
                                            subtotal=int(i['subtotal']),
                                            producto=idProd,
                                            venta=objVent.id)
                db.session.add(objDetalleVen)
                db.session.commit() 
    
            result = {"id": objVent.id}
            return jsonify(result)
            
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(message, 400)
    
@ventasRutas.route('/deleteVenta',methods=['GET','POST'])
@login_required
@roles_accepted('admin','vendedor')
def deleteVenta():
    try:
        if request.method == 'POST':
            idVent = int(request.form['idVenta'])
            ventaDel = db.session.query(venta).filter(venta.id == idVent).first()
            ventaDel.estatus='Inactivo'
            db.session.commit()
            
            detalleVen = db.session.query(detalle_venta).filter(detalle_venta.venta == idVent).all()
            for i in detalleVen:
                idProd = i.producto
                producto_upd = db.session.query(producto).filter(producto.id == idProd).first()
                producto_upd.cantidad = producto_upd.cantidad + i.cantidad
                
                db.session.commit() 

            result = {"id": idVent}
          
            return jsonify(result) 
            #return render_template('', ventas=ventasArray, activos = False)
            #return jsonify(message)
    
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(message, 400)


@ventasRutas.route('/getAllVentasHoy',methods=['GET','POST'])
@login_required
@roles_accepted('admin','vendedor')
def getAllVentasHoy():
    try:
        
        clientes = db.session.query(cliente,persona,domicilio).join(cliente.persona,persona.domicil).filter(persona.estatus == 'Activo').all()
        
        arrayProductos = list()
        productos = db.session.query(producto, categoria).join(producto.categoria).filter(producto.estatus == 'Activo').all()
        
        for i in productos:
            productoObj ={
                'idProducto': i.producto.id,
                'modelo': i.producto.modelo,
                'descripcion': i.producto.descripcion,
                'img': i.producto.img,
                'peso': i.producto.peso,
                'color': i.producto.color,
                'alto': i.producto.alto,
                'ancho': i.producto.ancho,
                'largo': i.producto.largo,
                'cantidad': i.producto.cantidad,
                'cantidad_minima': i.producto.cantidad_minima,
                'precio': i.producto.precio,
                'estatus': i.producto.estatus,
                'categoria':{
                    'id':i.categoria.id,
                    'nombre':i.categoria.nombre,
                    'descripcion':i.categoria.descripcion,
                    'estatus':i.categoria.estatus,
                }
            }
            arrayProductos.append(productoObj) 
            
        now = datetime.now()
        fechaHoy = now.strftime('%Y-%m-%d')
        ventasArray = list()
        ventas = db.session.query(venta).filter(venta.fecha_venta==fechaHoy, venta.estatus=='Activo').all()
        
        for i in ventas:
            persJson=personaSchema(many=False)
            produJson=ProductoSchema(many=False)
            detVenJson=Detalle_ventaSchema(many=False)
            ventJson=VentaSchema(many=False)
            clienJson=ClienteSchema(many=False)
            
            clientePers = db.session.query(cliente).filter(cliente.id==i.cliente).first()
            if clientePers:
                resCliente=clienJson.dump(clientePers)
                clientePers = db.session.query(persona).filter(persona.id==clientePers.idPersona).first()
                resCliente['idPersona'] = persJson.dump(clientePers)
            else:
                resCliente={}
                
            userSea = db.session.query(User).filter(User.id==i.user).first()
            if userSea:
                personUser = db.session.query(persona).filter(persona.id==userSea.idPersona).first()
                resUser=persJson.dump(personUser)
            else:
                resUser={}
            
            detalleVent = db.session.query(detalle_venta,producto).join(
                            detalle_venta.productoForegin).filter(detalle_venta.venta==i.id).all()
            detalleVentaArray = list()
            for j in detalleVent:
                objDetalle = detVenJson.dump(j.detalle_venta)
                objDetalle['producto']=produJson.dump(j.producto)
                
                detalleVentaArray.append(objDetalle)
            
            objVenta= ventJson.dump(i)
            objVenta['user']=resUser
            objVenta['cliente']=resCliente
            objVenta['detalleVenta']=detalleVentaArray

            ventasArray.append(objVenta)        

        return render_template('ventaDia.html', ventas=ventasArray, clientes=clientes, productos=arrayProductos)
        #return make_response(jsonify(ventasArray), 200)
    
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
