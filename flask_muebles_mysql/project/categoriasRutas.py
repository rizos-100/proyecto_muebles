from flask import Blueprint, render_template, jsonify, request
from .models import db, categoria, CategoriaSchema

categoriasRutas = Blueprint('categoriasRutas', __name__)


@categoriasRutas.route('/getAllCategoriasActivas', methods=['GET', 'POST'])
def getAllMaterialActivos():
     categoria_ = db.session.query(categoria).filter(categoria.estatus == "Activo").all()
     categoria_schema = CategoriaSchema(many=True)
     result = categoria_schema.dump(categoria_)
     return jsonify(result)
 
@categoriasRutas.route('/getAllCategoriasInactivas', methods=['GET', 'POST'])
def getAllCategoriasInactivas():
     categoria_ = db.session.query(categoria).filter(categoria.estatus == "Inactivo").all()
     categoria_schema = CategoriaSchema(many=True)
     result = categoria_schema.dump(categoria_)
     return jsonify(result)
 
@categoriasRutas.route('/getCategoriasPorNombre', methods=['GET', 'POST'])
def getCategoriasPorNombre():
     if request.method == 'GET':
          nombre = request.args.get("nombre", "No contiene el nombre")
          categoria_ = db.session.query(categoria).filter(categoria.nombre == nombre, categoria.estatus == "Activo").first()
          categoria_schema = CategoriaSchema(many=False)
          result = categoria_schema.dump(categoria_)
          return jsonify(result)

@categoriasRutas.route('/addCategoria', methods=['GET', 'POST'])
def addCategoria():
     if request.method == 'POST':
          nombre_ = request.form['nombre']
          descripcion_ = request.form['descripcion']
          
          cat = categoria(
                         nombre = nombre_,
                         descripcion = descripcion_,
                         estatus = "Activo")
          
          db.session.add(cat)
          db.session.commit()
          
          result = {"id": cat.id}
          
          return jsonify(result)
      
@categoriasRutas.route('/updateCategoria', methods=['GET', 'POST'])
def updateCategoria():
     if request.method == 'POST':
          id_ = request.form['id']
          nombre_ = request.form['nombre']
          descripcion_ = request.form['descripcion']
          
          categoria_ = db.session.query(categoria).filter(categoria.id == id_).first()
          categoria_.nombre = nombre_
          categoria_.descripcion = descripcion_

          db.session.commit()
          
          result = {"id": categoria_.id}
          
          return jsonify(result)

@categoriasRutas.route('/deleteCategoria', methods=['GET', 'POST'])
def deleteCategoria():
     if request.method == 'POST':
          id_ = request.form['id']
          
          categoria_ = db.session.query(categoria).filter(categoria.id == id_).first()
          categoria_.estatus = "Inactivo"

          db.session.commit()
          
          result = {"id": categoria_.id}
          
          return jsonify(result)