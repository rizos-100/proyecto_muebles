from flask import Blueprint, render_template, jsonify, request
from .models import db
from .models import material, MaterialSchema, sobrante_material, SobranteMaterialSchema
import json

materialRutas = Blueprint('materialRutas', __name__)

@materialRutas.route('/getAllMaterialDisponible', methods=['GET', 'POST'])
def getAllMaterialActivos():
     materiales = db.session.query(material).filter(material.estatus == "Disponible").all()
     return render_template("", materiales = materiales, activos = True)
     
@materialRutas.route('/getAllMaterialInutilizable', methods=['GET', 'POST'])
def getAllMaterialInactivos():
     materiales = db.session.query(material).filter(material.estatus == "Inutilizable").all()
     return render_template("", materiales = materiales, activos = False)

@materialRutas.route('/getMaterialPorId', methods=['GET', 'POST'])
def getMaterialPorId():
     if request.method == 'GET':
          id_ = request.args.get("id", "No contiene el nombre")
          materia = db.session.query(material).filter(material.id == id_,  material.estatus == "Disponible").all()
          return render_template("", material = materia, activos = True)
          
@materialRutas.route('/getAllSobranteDisponible', methods=['GET', 'POST'])
def getAllSobranteDisponible():
     sobrantes = db.session.query(sobrante_material).filter(sobrante_material.estatus == "Disponible").all()
     return render_template("", sobrantes = sobrantes, activos = True)

@materialRutas.route('/getAllSobranteInutilizable', methods=['GET', 'POST'])
def getAllSobranteInutilizable():
     sobrantes = db.session.query(sobrante_material).filter(sobrante_material.estatus == "Inutilizable").all()
     return render_template("", sobrantes = sobrantes, activos = False)


@materialRutas.route('/addMaterial', methods=['GET', 'POST'])
def addMaterial():
     if request.method == 'POST':
          nombre_ = request.form['nombre']
          tipo_ = request.form['tipo']
          descripcion_ = request.form['descripcion']
          cantidad_ = request.form['cantidad']
          alto_ = request.form['alto']
          ancho_ = request.form['ancho']
          grosor_ = request.form['grosor']
          color_ = request.form['color']
          
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
     
@materialRutas.route('/addSobrante', methods=['GET', 'POST'])
def addSobrante():
     if request.method == 'POST':
          alto_ = request.form['alto']
          ancho_ = request.form['ancho']
          comentario_ = request.form['comentario']
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
     

@materialRutas.route('/updateMaterial', methods=['GET', 'POST'])
def updateMaterial():
     if request.method == 'POST':
          id_ = request.form['id']
          nombre_ = request.form['nombre']
          tipo_ = request.form['tipo']
          descripcion_ = request.form['descripcion']
          cantidad_ = request.form['cantidad']
          alto_ = request.form['alto']
          ancho_ = request.form['ancho']
          grosor_ = request.form['grosor']
          color_ = request.form['color']
          
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
     
@materialRutas.route('/restarCantidadMaterial', methods=['GET', 'POST'])
def updateCantidadMaterial():
     if request.method == 'POST':
          id_ = request.form['id']
          cantidad_ = int(request.form['cantidad'])
          alto_ = int(request.form['alto'])
          ancho_ = int(request.form['ancho'])

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

@materialRutas.route('/updateSobrante', methods=['GET', 'POST'])
def updateSobrante():
     if request.method == 'POST':
          id_ = request.form['id']
          comentario_ = request.form['comentario']
          alto_ = request.form['alto']
          ancho_ = request.form['ancho']
          
          sobrante = db.session.query(sobrante_material).filter(sobrante_material.id == id_).first()

          sobrante.comentario = comentario_
          sobrante.alto = alto_
          sobrante.ancho = ancho_
          
          db.session.commit()
          
          result = {"id": sobrante.id}
          
          return jsonify(result)
     
@materialRutas.route('/deleteMaterial', methods=['GET', 'POST'])
def deleteMaterial():
     if request.method == 'POST':
          id_ = request.form['id']
          materia = db.session.query(material).filter(material.id == id_).first()
          materia.estatus = "Inutilizable"
          
          db.session.commit()
          
          result = {"id": materia.id}
          
          return jsonify(result)
     
@materialRutas.route('/deleteSobrante', methods=['GET', 'POST'])
def deleteSobrante():
     if request.method == 'POST':
          id_ = request.form['id']
          sobrante = db.session.query(sobrante_material).filter(sobrante_material.id == id_).first()
          sobrante.estatus = "Inutilizable"
          
          db.session.commit()
          
          result = {"id": sobrante.id}
          
          return jsonify(result)
         