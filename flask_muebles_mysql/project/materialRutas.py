from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db
from .models import material, MaterialSchema, sobrante_material, SobranteMaterialSchema,producto,detalle_producto_material as dpm,material
import json
import logging
from datetime import datetime
from project.validateInputs import validate as Validator

from flask_security import login_required
from flask_security.decorators import roles_required, roles_accepted

from .productoRutas import productoRutas

materialRutas = Blueprint('materialRutas', __name__)

@materialRutas.route('/getAllMaterialDisponibles', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllMaterialActivos():
     try:
          materiales = db.session.query(material).filter(material.estatus == "Disponible").all()
          return render_template("material.html", materiales = materiales, activos = True)
     except Exception as inst:
          message = {"result":"error"}
          logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
          return render_template('error.html')
     
@materialRutas.route('/getAllMaterialInutilizable', methods=['GET', 'POST'])
@login_required
def getAllMaterialInactivos():
     try:
          materiales = db.session.query(material).filter(material.estatus == "Inutilizable").all()
          return render_template("", materiales = materiales, activos = False)
     except Exception as inst:
          message = {"result":"error"}
          logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
          return render_template('error.html')

@materialRutas.route('/getMaterialPorId', methods=['GET', 'POST'])
@login_required
def getMaterialPorId():
     if request.method == 'GET':
          try:
               id_ = request.args.get("id", "No contiene el nombre")
               materia = db.session.query(material).filter(material.id == id_,  material.estatus == "Disponible").all()
               materia_schema = MaterialSchema(many=False)
               result = materia_schema.dump(materia)
               return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
          
@materialRutas.route('/getAllSobranteDisponible', methods=['GET', 'POST'])
@login_required
def getAllSobranteDisponible():
     try:
          sobrantes = db.session.query(sobrante_material).filter(sobrante_material.estatus == "Disponible").all()
          return render_template("", sobrantes = sobrantes, activos = True)
     except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')

@materialRutas.route('/getAllSobranteInutilizable', methods=['GET', 'POST'])
@login_required
def getAllSobranteInutilizable():
     try:
          sobrantes = db.session.query(sobrante_material).filter(sobrante_material.estatus == "Inutilizable").all()
          return render_template("", sobrantes = sobrantes, activos = False)
     except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
           
@materialRutas.route('/getSobranteDisponiblePorId', methods=['GET', 'POST'])
@login_required
def getSobranteDisponiblePorId():
     if request.method == 'GET':
          try:
               id_ = request.args.get("id", "No contiene el nombre")
               sobrantes = db.session.query(sobrante_material).filter(sobrante_material.id == id_, sobrante_material.estatus == "Disponible").all()
               return render_template("", sobrantes = sobrantes, activos = False)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')


@materialRutas.route('/addMaterial', methods=['GET', 'POST'])
@login_required
def addMaterial():
     if request.method == 'POST':
          try:
               nombre_ = Validator.sanitizarNombre(request.form['nombre'])
               tipo_ = Validator.sanitizarNombre(request.form['tipo'])
               descripcion_ = Validator.sanitizarNombre(request.form['descripcion'])
               cantidad_ = Validator.validarDecimal(request.form['cantidad'])
               alto_ = Validator.validarDecimal(request.form['alto'])
               ancho_ = Validator.validarDecimal(request.form['ancho'])
               grosor_ = Validator.validarDecimal(request.form['grosor'])
               color_ = Validator.sanitizarNombre(request.form['color'])
               
               mat = material(tipo = tipo_,
                              nombre = nombre_,
                              descripcion = descripcion_,
                              cantidad = cantidad_,
                              alto = alto_,
                              ancho = ancho_,
                              grosor = grosor_,
                              color = color_,
                              estatus = "Disponible")
               
               db.session.add(mat)
               db.session.commit()
               
               result = {"id": mat.id}
               
               return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
           
@materialRutas.route('/addSobrante', methods=['GET', 'POST'])
@login_required
def addSobrante():
     if request.method == 'POST':
          try:
               alto_ = Validator.validarDecimal(request.form['alto'])
               ancho_ = Validator.validarDecimal(request.form['ancho'])
               comentario_ = Validator.sanitizarNombre(request.form['comentario'])
               id_material = request.form['id_material']
               
               sobrante = sobrante_material(alto = alto_,
                                        ancho = ancho_,
                                        comentario = comentario_,
                                        estatus = "Disponible",
                                        material = id_material)
               
               db.session.add(sobrante)
               db.session.commit()
               
               result = {"id": sobrante.id}
               
               return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
     

@materialRutas.route('/updateMaterial', methods=['GET', 'POST'])
@login_required
def updateMaterial():
     if request.method == 'POST':
          try:
               id_ = request.form['id']
               nombre_ = Validator.sanitizarNombre(request.form['nombre'])
               tipo_ = Validator.sanitizarNombre(request.form['tipo'])
               descripcion_ = Validator.sanitizarNombre(request.form['descripcion'])
               cantidad_ = Validator.validarDecimal(request.form['cantidad'])
               alto_ = Validator.validarDecimal(request.form['alto'])
               ancho_ = Validator.validarDecimal(request.form['ancho'])
               grosor_ = Validator.validarDecimal(request.form['grosor'])
               color_ = Validator.sanitizarNombre(request.form['color'])
               
               materia = db.session.query(material).filter(material.id == id_).first()
               materia.nombre = nombre_
               materia.tipo = tipo_
               materia.descripcion = descripcion_
               materia.cantidad = cantidad_
               materia.alto = alto_
               materia.ancho = ancho_
               materia.grosor = grosor_
               materia.color = color_
               
               db.session.commit()
               
               result = {"id": materia.id}
               
               return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
     
@materialRutas.route('/restarCantidadMaterial', methods=['GET', 'POST'])
@login_required
def updateCantidadMaterial():
     if request.method == 'POST':
          try:
               id_ = request.form['id']
               cantidad_ = Validator.validarDecimal(request.form['cantidad'])
               alto_ = Validator.validarDecimal(request.form['alto'])
               ancho_ = Validator.validarDecimal(request.form['ancho'])

               materia = db.session.query(material).filter(material.id == id_).first()

               if materia.cantidad >= cantidad_ and materia.alto >= alto_ and materia.ancho >= ancho_:
                    materia.cantidad = materia.cantidad - cantidad_
                    materia.alto =  materia.alto - alto_
                    materia.ancho = materia.ancho - ancho_
                    db.session.commit()
                    
                    result = {"id": materia.id}
               
                    return jsonify(result)
               else:
                    result = {"id": "El material con id: " + str(materia.id) + " no es suficiente"}
               
                    return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')     

@materialRutas.route('/updateSobrante', methods=['GET', 'POST'])
@login_required
def updateSobrante():
     if request.method == 'POST':
          try:
               id_ = request.form['id']
               comentario_ = Validator.sanitizarNombre(request.form['comentario'])
               alto_ = Validator.validarDecimal(request.form['alto'])
               ancho_ = Validator.validarDecimal(request.form['ancho'])
               
               sobrante = db.session.query(sobrante_material).filter(sobrante_material.id == id_).first()

               sobrante.comentario = comentario_
               sobrante.alto = alto_
               sobrante.ancho = ancho_
               
               db.session.commit()
               
               result = {"id": sobrante.id}
               
               return jsonify(result)
          except Exception as inst:
                message = {"result":"error"}
                logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
                return render_template('error.html')
     
@materialRutas.route('/deleteMaterial', methods=['GET', 'POST'])
@login_required
def deleteMaterial():
     if request.method == 'POST':
          try:
               id_ = request.form['id']
               materia = db.session.query(material).filter(material.id == id_).first()
               materia.estatus = "Inutilizable"
               
               db.session.commit()
               
               result = {"id": materia.id}
               
               return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
     
@materialRutas.route('/deleteSobrante', methods=['GET', 'POST'])
@login_required
def deleteSobrante():
     if request.method == 'POST':
          try:
               id_ = request.form['id']
               sobrante = db.session.query(sobrante_material).filter(sobrante_material.id == id_).first()
               sobrante.estatus = "Inutilizable"
               
               db.session.commit()
               
               result = {"id": sobrante.id}
               
               return jsonify(result)
          except Exception as inst:
               message = {"result":"error"}
               logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
               return render_template('error.html')
         

@materialRutas.route('/getAllMaterialRecomendado', methods=['GET', 'POST'])
#@login_required
#@roles_accepted('admin','almacenista','vendedor')
def getAllMaterialRecomendado():
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
               
          return make_response(jsonify(arrayRecList),200)
          #return render_template("material.html", materiales = materiales, activos = True)
     except Exception as inst:
          message = {"result":"error"}
          logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
          return render_template('error.html')