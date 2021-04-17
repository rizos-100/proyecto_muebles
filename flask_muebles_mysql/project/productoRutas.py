from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db, producto, ProductoSchema, categoria,CategoriaSchema, material, detalle_producto_material, sobrante_material
import logging
from datetime import datetime
from project.validateInputs import validate as Validator
import os

from flask_security import login_required
from flask_security.decorators import roles_accepted

productoRutas = Blueprint('productoRutas', __name__)

FOLDER = os.path.abspath('project/static/img/')

@productoRutas.route('/getAllProductosActivos', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista','vendedor')
def getAllProductosActivos():
    try:
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
        return render_template("productos.html", productos = arrayProductos, activos = True)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
        
@productoRutas.route('/getAllProductosInactivos', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista','vendedor')
def getAllProductosInactivos():
    try:
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
        return render_template("productos.html", productos = arrayProductos, activos = False)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@productoRutas.route('/getAllProductosPorId', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def getAllProductosPorId():
    try:
        arrayProductos = list()
        id_ = request.args.get("id", "No contiene el nombre")
        productos = db.session.query(producto, categoria).join(producto.categoria).filter(producto.id == id_, producto.estatus == 'Activo').all()
        
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
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@productoRutas.route('/addProducto', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def addProducto():
        if request.method == 'POST':
            try:
                modelo_ = Validator.sanitizarNombre(request.form['modelo'])
                descripcion_ = Validator.sanitizarNombre(request.form['descripcion'])
                img_ = request.form['img']
                

                #filename = img_.filename
                #if filename != None and filename != "":
                    #img_.save(os.path.join(FOLDER, filename))
                
                
                peso_ = Validator.validarDecimal(request.form['peso'])
                color_ = Validator.sanitizarNombre(request.form['color'])
                alto_ = Validator.validarDecimal(request.form['alto'])
                ancho_ = Validator.validarDecimal(request.form['ancho'])
                largo_ = Validator.validarDecimal(request.form['largo'])
                cantidad_ = Validator.validarDecimal(request.form['cantidad'])
                cantidad_minima_ = Validator.validarDecimal(request.form['cantidad_minima'])
                precio_ = Validator.validarDecimal(request.form['precio'])
                
                
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
            except Exception as inst:
                message = {"result":"error"}
                logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
                return render_template('error.html')
    
@productoRutas.route('/updateProducto', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def updateProducto():
    if request.method == 'POST':
        try:
            idProducto_ = request.form['idProducto']
            modelo_ = Validator.sanitizarNombre(request.form['modelo'])
            descripcion_ = Validator.sanitizarNombre(request.form['descripcion'])
            img_ = request.form['img']
            
            #filename = img_.filename
            #if filename != None and filename != "":
                #img_.save(os.path.join(FOLDER, filename))
            
            
            peso_ =Validator.validarDecimal(request.form['peso'])
            color_ = Validator.sanitizarNombre(request.form['color'])
            alto_ = Validator.validarDecimal(request.form['alto'])
            ancho_ = Validator.validarDecimal(request.form['ancho'])
            largo_ = Validator.validarDecimal(request.form['largo'])
            cantidad_minima_ = Validator.validarDecimal(request.form['cantidad_minima'])
            precio_ = Validator.validarDecimal(request.form['precio'])
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
        except Exception as inst:
                message = {"result":"error"}
                logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
                return render_template('error.html')
        
@productoRutas.route('/updateStockProducto', methods=['GET', 'POST'])
def updateStockProducto():
    if request.method == 'POST':
        try:
            idProducto_ = request.form['idProducto']
            cantidad_ = Validator.validarDecimal(request.form['cantidad'])

            p = db.session.query(producto).filter(
            producto.id == idProducto_).first()
            p.cantidad = p.cantidad + float(cantidad_)
            #db.session.commit()

            bb = True
            z = 0
            while z < float(cantidad_):

                #Consultar detalles producto materil del producto
                dtmp = db.session.query(detalle_producto_material).filter(detalle_producto_material.idProducto == idProducto_).all()
                print(dtmp)
                #Consultamos el material de ese detalle
                arraySobrantes = []
                for i in dtmp:
                    #Si es madera, se busca en los sobrantes
                    if i.alto != 0 and i.ancho != 0:  # Si cumple la condicion es madera
                        #Buscar en los sobrantes
                        s = db.session.query(sobrante_material).filter(sobrante_material.alto >= float(i.alto), sobrante_material.ancho >= float(i.ancho), sobrante_material.estatus == "Disponible").first()
                        #Si se encuentra, se descuenta
                        if s != None:
                            s.alto = s.alto - float(i.alto)
                            s.ancho = s.ancho - float(i.ancho)
                            print("entre")
                            if s.alto <= .5 and s.ancho <= .5:
                                s.estatus = "Inutilizable"
                            #db.session.commit()
                        else:  # Sino, busca la madera en material y la descuenta
                            m = db.session.query(material).filter(material.id == i.idMaterial).first()
                        #Descuento de material
                            if m.cantidad > 0:
                                m.cantidad = m.cantidad - 1
                                
                                alto_ = m.alto - float(i.alto)
                                ancho_ = m.ancho - float(i.ancho)
                                comentario_ = "ninguno"
                                id_material = m.id
                                
                                sobrante = sobrante_material(alto = alto_,
                                        ancho = ancho_,
                                        comentario = comentario_,
                                        estatus = "Disponible",
                                        material = id_material)
                                
                                arraySobrantes.append(sobrante)

                                result = {"id": p.id}
                            else:
                                bb = False
                                result = {"error": "El material con id: " + str(m.id) + " no tiene suficientes tablones y no se realizo ningun cambio"}
                    else:  # Sino cumple la condicion de que es madera, descuenta la cantidad de material
                        m = db.session.query(material).filter(
                            material.id == i.idMaterial).first()
                        #Descuento de material
                        if m.cantidad >= float(i.cantidad) and m.cantidad != 0:
                            m.cantidad = m.cantidad - float(i.cantidad)
                            #db.session.commit()
                            result = {"id": p.id}
                        else:
                            bb = False
                            result = {"error": "El material con id: " + str(m.id) + " no es suficiente y no se realizo ningun cambio"}
                z += 1
            if bb != False:
                for so in arraySobrantes:
                    db.session.add(so)
                    db.session.commit()
                db.session.commit()
            else:
                result = {"error": "No hay material suficiente para esa cantidad y no se realizo ningun cambio"}

            return jsonify(result)
        except Exception as inst:
            message = {"result": "error"}
            logging.error(str(type(inst))+'\n Tipo de error: ' +
                          str(inst) + '['+str(datetime.now())+']')
            return render_template('error.html')
    
@productoRutas.route('/deleteProducto', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista')
def deleteProducto():
    if request.method == 'POST':
        try:
            idProducto_ = request.form['idProducto']
            p = db.session.query(producto).filter(producto.id == idProducto_).first()
            p.estatus = "Inactivo"
            
            db.session.commit()
            
            result = {"id": p.id}
            
            return jsonify(result)
        except Exception as inst:
                message = {"result":"error"}
                logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
                return render_template('error.html')
    

@productoRutas.route('/getAllProductosRecomendados', methods=['GET','POST'])
@login_required
@roles_accepted('admin','almacenista','vendedor')
def getAllProductosRecomendados():
    try:
        prodJson = ProductoSchema(many=False)
        cateJson = CategoriaSchema(many=False)
        arrayProductos = list()
        productos = db.session.query(producto, categoria).join(producto.categoria).filter(producto.estatus == 'Activo').all()
        
        for i in productos:
            if i.producto.cantidad < i.producto.cantidad_minima:
                productoObj = prodJson.dump(i.producto)
                productoObj['idCategoria'] = cateJson.dump(i.categoria)
                productoObj['cantRecomend'] = i.producto.cantidad_minima - i.producto.cantidad;
            
                arrayProductos.append(productoObj) 
        
        return make_response(jsonify(arrayProductos),200)
        #return render_template("", productos = arrayProductos, activos = True)
        
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')
        

