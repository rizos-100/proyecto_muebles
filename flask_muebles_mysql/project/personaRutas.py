from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db
from .models import persona,personaSchema,domicilio,DomicilioSchema
from project.validateInputs import validate as Validator

from flask_security import login_required
from flask_security.decorators import roles_required, roles_accepted

import logging
from datetime import datetime

personasRutas = Blueprint('personasRutas', __name__ )

@personasRutas.route('/getAllPersonasActivas',methods=['GET','POST'])
#@login_required
#@roles_accepted('admin','vendedor')
def getAllPersonasActivas():
    try:
        arrayPersonas = list()
        peronas = db.session.query(persona).filter(persona.estatus == 'Activo').all()
        for per in peronas:
            perJson = personaSchema(many=False).dump(per)
            domi = db.session.query(domicilio).filter(domicilio.id==per.domicilio).first()
            perJson['domicilio'] = DomicilioSchema(many=False).dump(domi)
            
            arrayPersonas.append(perJson)
        
        #return render_template('', peronas=peronas, activos = True)
        return make_response(jsonify(arrayPersonas), 200)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')




