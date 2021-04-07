from flask import Blueprint, render_template, jsonify, request
from .models import db
from .models import cliente,persona,domicilio
import json

clienteRutas = Blueprint('clienteRutas', __name__)

@clienteRutas.route('/getAllClientes',methods=['GET','POST'])
def getAllClientes():
    arrayClientes = list()
    clientes = db.session.query(cliente,persona,domicilio).join(cliente.persona,persona.domicil).filter(persona.estatus == 'Activo').all()
    
    for i in clientes:
        clienObj ={
            'idCliente': i.cliente.id,
            'persona':{
                'id':i.persona.id,
                'nombre':i.persona.nombre,
                'apellidoP':i.persona.apellidoP,
                'apellidoM':i.persona.apellidoM,
                'numFijo':i.persona.numero_fijo,
                'celular':i.persona.celular,
                'rfc':i.persona.rfc
            },
            'domicilio':{
                'id':i.domicilio.id,
                'calle':i.domicilio.calle,
                'colonia':i.domicilio.colonia,
                'numero_interior':i.domicilio.numero_interior,
                'municipio':i.domicilio.municipio,
                'cp':i.domicilio.cp,
                'referencias':i.domicilio.referencias
            }
        }
        arrayClientes.append(clienObj) 
    return jsonify(arrayClientes)

@clienteRutas.route('/addCliente', methods=['GET', 'POST'])
def addCliente():
     if request.method == 'POST':
          nombre_ = request.form['nombre']
          apellidoP_ = request.form['apellidoP']
          apellidoM_ = request.form['apellidoM']
          numero_fijo_ = request.form['numero_fijo']
          celular_ = request.form['celular']
          rfc_ = request.form['rfc']
          
          calle_ = request.form['calle']
          colonian_ = request.form['colonia']
          numero_interior_ = request.form['numero_interior']
          numero_exterior_ = request.form['numero_exterior']
          estado_ = request.form['estado']
          municipio_ = request.form['municipio']
          cp_ = request.form['cp']
          referencias_ = request.form['referencias']
          
          objDomicilio = domicilio(calle=calle_,
                                    colonia=colonian_,
                                    numero_interior=numero_interior_,
                                    numero_exterior=numero_exterior_,
                                    estado=estado_,
                                    municipio=municipio_,
                                    cp=cp_,
                                    referencias=referencias_,
                                    estatus=1)
          
          db.session.add(objDomicilio)
          db.session.commit()
          idDom= objDomicilio.id
          
          objPersona = persona(nombre=nombre_,
                                apellidoP=apellidoP_,
                                apellidoM=apellidoM_,
                                numero_fijo=numero_fijo_,
                                celular=celular_,
                                estatus='Activo',
                                domicilio=idDom,
                                rfc=rfc_)
          
          db.session.add(objPersona)
          db.session.commit()
          idPers=objPersona.id 
          
          objCliente = cliente(idPersona=idPers)
          db.session.add(objCliente)
          db.session.commit()
          
          result = {"id": objCliente.id}
          
          return jsonify(result)
      
@clienteRutas.route('/updateCliente', methods=['GET', 'POST'])
def updateCliente():
    
     if request.method == 'POST':
         
          idPers = request.form['idP']
          nombre_ = request.form['nombre']
          apellidoP_ = request.form['apellidoP']
          apellidoM_ = request.form['apellidoM']
          numero_fijo_ = request.form['numero_fijo']
          celular_ = request.form['celular']
          rfc_ = request.form['rfc']
          
          idDom = request.form['idD']
          calle_ = request.form['calle']
          colonian_ = request.form['colonia']
          numero_interior_ = request.form['numero_interior']
          numero_exterior_ = request.form['numero_exterior']
          estado_ = request.form['estado']
          municipio_ = request.form['municipio']
          cp_ = request.form['cp']
          referencias_ = request.form['referencias']
          
          domicilio_upd = db.session.query(domicilio).filter(domicilio.id == idDom).first()
          domicilio_upd.calle=calle_
          domicilio_upd.colonia=colonian_
          domicilio_upd.numero_interior=numero_interior_
          domicilio_upd.numero_exterior=numero_exterior_
          domicilio_upd.estado=estado_
          domicilio_upd.municipio=municipio_
          domicilio_upd.cp=cp_
          domicilio_upd.referencias=referencias_

          db.session.commit()
          
          persona_upd = db.session.query(persona).filter(persona.id == idPers).first()
          persona_upd.nombre=nombre_
          persona_upd.apellidoP=apellidoP_
          persona_upd.apellidoM=apellidoM_
          persona_upd.numero_fijo=numero_fijo_
          persona_upd.celular=celular_
          persona_upd.rfc=rfc_
        
          db.session.commit()
        
          result = {"id": persona_upd.id}
          
          return jsonify(result)

@clienteRutas.route('/deleteCliente', methods=['GET', 'POST'])
def deleteCliente():
    
     if request.method == 'POST':
         
          idPers = request.form['idP']
          
          persona_upd = db.session.query(persona).filter(persona.id == idPers).first()
          persona_upd.estatus='Inactivo'
        
          db.session.commit()
        
          result = {"id": persona_upd.id}
          
          return jsonify(result)
