from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db
from .models import cliente,persona,personaSchema,User,venta,VentaSchema,detalle_venta,Detalle_ventaSchema,producto,ProductoSchema
import json

ventasRutas = Blueprint('ventasRutas', __name__)

@ventasRutas.route('/getAllVentas',methods=['GET','POST'])
def getAllVentas():
    ventasArray = list()
    ventas = db.session.query(venta).all()
    
    for i in ventas:
        persJson=personaSchema(many=False)
        produJson=ProductoSchema(many=False)
        detVenJson=Detalle_ventaSchema(many=False)
        ventJson=VentaSchema(many=False)
        
        personCliente = db.session.query(persona).filter(persona.id==i.cliente).first()
        resCliente=persJson.dump(personCliente)
        
        userSea = db.session.query(User).filter(User.id==i.user).first()
        personUser = db.session.query(persona).filter(persona.id==userSea.idPersona).first()
        resUser=persJson.dump(personUser)
        
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

    return make_response(jsonify(ventasArray), 200)
