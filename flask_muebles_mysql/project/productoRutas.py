from flask import Blueprint, render_template, jsonify, request
from .models import db, producto, ProductoSchema, categoria

productoRutas = Blueprint('productoRutas', __name__)

@productoRutas.route('/getAllProductosActivos', methods=['GET','POST'])
def getAllProductosActivos():
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
    return jsonify(arrayProductos)

@productoRutas.route('/getAllProductosInactivos', methods=['GET','POST'])
def getAllProductosInactivos():
    arrayProductos = list()
    productos = db.session.query(producto, categoria).join(producto.categoria).filter(producto.estatus == 'Inactivo').all()
    
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
    return jsonify(arrayProductos)

@productoRutas.route('/addProducto', methods=['GET','POST'])
def addProducto():
    if request.method == 'POST':
        modelo_ = request.form['modelo']
        descripcion_ = request.form['descripcion']
        img_ = request.form['img']
        peso_ = request.form['peso']
        color_ = request.form['color']
        alto_ = request.form['alto']
        ancho_ = request.form['ancho']
        largo_ = request.form['largo']
        cantidad_ = request.form['cantidad']
        cantidad_minima_ = request.form['cantidad_minima']
        precio_ = request.form['precio']
        
        
        idCategoria_ = request.form['idCategoria']
        
        prod = producto(modelo = modelo_,
                        descripcion = descripcion_,
                        img = img_,
                        peso = peso_,
                        color = color_,
                        alto = alto_,
                        ancho = ancho_,
                        largo = largo_,
                        cantidad = cantidad_,
                        cantidad_minima = cantidad_minima_,
                        precio = precio_,
                        estatus = "Activo",
                        idCategoria = idCategoria_)
        
        db.session.add(prod)
        db.session.commit()
        
        result = {"id": prod.id}
          
        return jsonify(result)
    
@productoRutas.route('/updateProducto', methods=['GET','POST'])
def updateProducto():
    if request.method == 'POST':
        idProducto_ = request.form['idProducto']
        modelo_ = request.form['modelo']
        descripcion_ = request.form['descripcion']
        img_ = request.form['img']
        peso_ = request.form['peso']
        color_ = request.form['color']
        alto_ = request.form['alto']
        ancho_ = request.form['ancho']
        largo_ = request.form['largo']
        cantidad_minima_ = request.form['cantidad_minima']
        precio_ = request.form['precio']
        idCategoria_ = request.form['idCategoria']
        
        p = db.session.query(producto).filter(producto.id == idProducto_).first()
        c = db.session.query(categoria).filter(categoria.id == idCategoria_).first()
        p.modelo = modelo_
        p.descripcion = descripcion_
        p.img = img_
        p.peso = peso_
        p.color = color_
        p.alto = alto_
        p.ancho = ancho_
        p.largo = largo_
        p.cantidad_minima = cantidad_minima_
        p.precio = precio_
        p.idCategoria = c.id
        p.categoria = c
                
        db.session.commit()
        
        db.session.commit()
        
        result = {"id": p.id}
          
        return jsonify(result)
    
@productoRutas.route('/updateStockProducto', methods=['GET','POST'])
def updateStockProducto():
    if request.method == 'POST':
        idProducto_ = request.form['idProducto']
        cantidad_ = request.form['cantidad']

        p = db.session.query(producto).filter(producto.id == idProducto_).first()
        p.cantidad = cantidad_
        
        db.session.commit()
        
        db.session.commit()
        
        result = {"id": p.id}
          
        return jsonify(result)
        
@productoRutas.route('/deleteProducto', methods=['GET','POST'])
def deleteProducto():
    if request.method == 'POST':
        idProducto_ = request.form['idProducto']
        p = db.session.query(producto).filter(producto.id == idProducto_).first()
        p.estatus = "Inactivo"
        
        db.session.commit()
        
        result = {"id": p.id}
          
        return jsonify(result)