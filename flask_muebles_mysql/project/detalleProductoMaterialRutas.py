from flask import Blueprint, render_template, jsonify, request
from .models import db, detalle_producto_material, producto, material, Detalle_produco_material_Schema

detalleProductoMaterialRutas = Blueprint('detalleProductoMaterialRutas', __name__)

@detalleProductoMaterialRutas.route('/getAllDetalleProductosMaterial', methods=['GET','POST'])
def getAllDetalleProductosMaterial():
    if request.method == 'GET':
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
    return jsonify(arrayDPM)


@detalleProductoMaterialRutas.route('/addDetalleProductosMaterial', methods=['GET','POST'])
def addDetalleProductosMaterial():
    if request.method == 'POST':
          alto_ = request.form['alto']
          ancho_ = request.form['ancho']
          cantidad_ = request.form['cantidad']
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