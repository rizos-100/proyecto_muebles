from flask import Blueprint, render_template, jsonify, request
from .models import db
from .models import cliente,persona,domicilio
import json

ventasRutas = Blueprint('ventasRutas', __name__)

@ventasRutas.route('/getAllVentas',methods=['GET','POST'])
def getAllVentas():
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
