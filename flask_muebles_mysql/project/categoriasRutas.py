from flask import Blueprint, render_template, jsonify, request
from .models import db, categoria, CategoriaSchema
from project.validateInputs import validate as Validator

from flask_security import login_required
from flask_security.decorators import roles_accepted

categoriasRutas = Blueprint('categoriasRutas', __name__)


@categoriasRutas.route('/getAllCategoriasActivas', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllMaterialActivos():
     categoria_ = db.session.query(categoria).filter(categoria.estatus == "Activo").all()
     return render_template('categoria.html', categorias=categoria_, activos = True)
 
@categoriasRutas.route('/getAllCategoriasInactivas', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllCategoriasInactivas():
     categoria_ = db.session.query(categoria).filter(categoria.estatus == "Inactivo").all()
     return render_template('categoria.html', categorias=categoria_, activos = False)
 
@categoriasRutas.route('/getSelectCategorias', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def getSelectCategorias():
     categoria_ = db.session.query(categoria).filter(categoria.estatus == "Activo").all()
     categoria_schema = CategoriaSchema(many=True)
     result = categoria_schema.dump(categoria_)
     return jsonify(result)

@categoriasRutas.route('/getCategoriasPorId', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def getCategoriasPorId():
     if request.method == 'GET':
          idC = request.args.get("idCat", "No contiene el nombre")
          categoria_ = db.session.query(categoria).filter(categoria.id == idC, categoria.estatus == "Activo").first()
          categoria_schema = CategoriaSchema(many=False)
          result = categoria_schema.dump(categoria_)
          return jsonify(result)

@categoriasRutas.route('/addCategoria', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def addCategoria():
     if request.method == 'POST':
          nombre_ = Validator.sanitizarNombre(request.form['nombre'])
          descripcion_ = Validator.sanitizarNombre(request.form['descripcion'])
          
          cat = categoria(
                         nombre = nombre_,
                         descripcion = descripcion_,
                         estatus = "Activo")
          
          db.session.add(cat)
          db.session.commit()
          
          result = {"id": cat.id}
          
          return jsonify(result)
      
@categoriasRutas.route('/updateCategoria', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def updateCategoria():
     if request.method == 'POST':
          id_ = request.form['id']
          nombre_ = Validator.sanitizarNombre(request.form['nombre'])
          descripcion_ = Validator.sanitizarNombre(request.form['descripcion'])
          
          categoria_ = db.session.query(categoria).filter(categoria.id == id_).first()
          categoria_.nombre = nombre_
          categoria_.descripcion = descripcion_

          db.session.commit()
          
          result = {"id": categoria_.id}
          
          return jsonify(result)

@categoriasRutas.route('/deleteCategoria', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin','almacenista')
def deleteCategoria():
     if request.method == 'POST':
          id_ = request.form['id']
          
          categoria_ = db.session.query(categoria).filter(categoria.id == id_).first()
          categoria_.estatus = "Inactivo"

          db.session.commit()
          
          result = {"id": categoria_.id}
          
          return jsonify(result)