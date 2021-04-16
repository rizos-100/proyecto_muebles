from flask import Blueprint, render_template, jsonify, request,make_response
from .models import db
from .models import persona,personaSchema,domicilio,DomicilioSchema,User,UserSchema,cliente, users_roles, Role
from project.validateInputs import validate as Validator

from flask_security import login_required
from flask_security.decorators import roles_accepted

import logging
from datetime import datetime

empleadoRutas = Blueprint('empleadoRutas', __name__ )

@empleadoRutas.route('/getAllEmpleadosSinAsignar',methods=['GET','POST'])
@login_required
@roles_accepted('admin')
def getAllEmpleadosSinAsignar():
    try:
        arrayPersonas = list()
        personas = db.session.query(persona).filter(persona.estatus == 'Activo').all()
        
        for per in personas:
            userPer = db.session.query(User).filter(User.idPersona == per.id).first()
            clienPer = db.session.query(cliente).filter(cliente.idPersona == per.id).first()
            if not userPer and not clienPer:
                print(per)
                perJson = personaSchema(many=False).dump(per)
                domi = db.session.query(domicilio).filter(domicilio.id==per.domicilio).first()
                perJson['domicilio'] = DomicilioSchema(many=False).dump(domi)
                
                arrayPersonas.append(perJson)
        
        return render_template('empleado_sin_asignar.html', personas=arrayPersonas, activos = True)
        #return make_response(jsonify(arrayPersonas), 200)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@empleadoRutas.route('/getAllEmpleadosActivos',methods=['GET','POST'])
#@login_required
#@roles_accepted('admin')
def getAllEmpleadosActivos():
    try:
        arrayUser = list()
        personas = db.session.query(persona,User).join(User.personaForeign).filter(persona.estatus == 'Activo').all()

        for per in personas:
            perJson = personaSchema(many=False).dump(per.persona)
            useJson = UserSchema(many=False).dump(per.User)
            id= useJson['id']
            domi = db.session.query(domicilio).filter(domicilio.id==per.persona.domicilio).first()
            us = db.session.query(User, Role).join(User.roles).filter(User.id == id).all()
            role = {
                "id_role": us[0][1].id,
                "name": us[0][1].name
            }
            perJson['domicilio'] = DomicilioSchema(many=False).dump(domi)
            useJson['idPersona'] = perJson
            useJson['role'] = role
                
            arrayUser.append(useJson)   
        
        return render_template('empleado.html', empleados=arrayUser, activos=True)
        #return make_response(jsonify(arrayUser), 200)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@empleadoRutas.route('/getAllEmpleadosInactivos',methods=['GET','POST'])
@login_required
@roles_accepted('admin')
def getAllEmpleadosInactivos():
    try:
        arrayUser = list()
        personas = db.session.query(persona,User).join(User.personaForeign).filter(persona.estatus == 'Inactivo').all()

        for per in personas:
            print(per)
            perJson = personaSchema(many=False).dump(per.persona)
            useJson = UserSchema(many=False).dump(per.User)
            id= useJson['id']
            domi = db.session.query(domicilio).filter(domicilio.id==per.persona.domicilio).first()
            us = db.session.query(User, Role).join(User.roles).filter(User.id == id).all()
            role = {
                "id_role": us[0][1].id,
                "name": us[0][1].name
            }
            perJson['domicilio'] = DomicilioSchema(many=False).dump(domi)
            useJson['idPersona'] = perJson
            useJson['role'] = role
                
            arrayUser.append(useJson)
        
        return render_template('empleado.html', empleados=arrayUser, activos =False)
        #return make_response(jsonify(arrayUser), 200)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@empleadoRutas.route('/getAllEmpleadosById',methods=['GET','POST'])
@login_required
@roles_accepted('admin')
def getAllEmpleadosById():
    try:
        if request.method == 'GET':
            arrayPersonas = list()
            idPer = int(request.args.get('idPersona','0'))
            arrayUser = list()
            personas = db.session.query(persona).filter(persona.estatus == 'Activo', persona.id == idPer).all()
            for per in personas:
                perJson = personaSchema(many=False).dump(per)
                domi = db.session.query(domicilio).filter(domicilio.id==per.domicilio).first()
                perJson['domicilio'] = DomicilioSchema(many=False).dump(domi)
                
                arrayPersonas.append(perJson)
            
            return jsonify(arrayPersonas[0])
            #return make_response(jsonify(arrayPersonas), 200)
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return render_template('error.html')

@empleadoRutas.route('/addEmpleado', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def addEmpleado():
    try:
        if request.method == 'POST':
          nombre_ = Validator.sanitizarNombre(request.form['nombre'])
          apellidoP_ = Validator.sanitizarNombre(request.form['apellidoP'])
          apellidoM_ = Validator.sanitizarNombre(request.form['apellidoM'])
          numero_fijo_ = Validator.validarTel(request.form['numero_fijo'])
          celular_ = Validator.validarTel(request.form['celular'])
          rfc_ = Validator.validarRFC(request.form['rfc'])
          
          calle_ = Validator.sanitizarNombre(request.form['calle'])
          colonian_ = Validator.sanitizarNombre(request.form['colonia'])
          numero_interior_ = Validator.validarNumDireccion(request.form['numero_interior'])
          numero_exterior_ = Validator.validarNumDireccion(request.form['numero_exterior'])
          estado_ = Validator.sanitizarNombre(request.form['estado'])
          municipio_ = Validator.sanitizarNombre(request.form['municipio'])
          cp_ = int(request.form['cp'])
          referencias_ = Validator.sanitizarNombre(request.form['referencias'])
          
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
          
          
          result = {"id": idPers}
          
          return result
      
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)
 
@empleadoRutas.route('/updateEmpleado', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def updateEmpleado():
    try:
        if request.method == 'POST':
         
            idPers = int(request.form['idP'])
            nombre_ = Validator.sanitizarNombre(request.form['nombre'])
            apellidoP_ = Validator.sanitizarNombre(request.form['apellidoP'])
            apellidoM_ = Validator.sanitizarNombre(request.form['apellidoM'])
            numero_fijo_ = Validator.validarTel(request.form['numero_fijo'])
            celular_ = Validator.validarTel(request.form['celular'])
            rfc_ = Validator.validarRFC(request.form['rfc'])
            
            idDom = int(request.form['idD'])
            calle_ = Validator.sanitizarNombre(request.form['calle'])
            colonian_ = Validator.sanitizarNombre(request.form['colonia'])
            numero_interior_ = Validator.validarNumDireccion(request.form['numero_interior'])
            numero_exterior_ = Validator.validarNumDireccion(request.form['numero_exterior'])
            estado_ = Validator.sanitizarNombre(request.form['estado'])
            municipio_ = Validator.sanitizarNombre(request.form['municipio'])
            cp_ = request.form['cp']
            referencias_ = Validator.sanitizarNombre(request.form['referencias'])
            
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
          
          #return make_response(jsonify(result),200)
            return result
      
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)    


@empleadoRutas.route('/deleteEmpleado', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def deleteEmpleado():
    try:
        if request.method == 'POST':
         
          idPers = int(request.form['idP'])
          
          persona_upd = db.session.query(persona).filter(persona.id == idPers).first()
          persona_upd.estatus='Inactivo'
        
          db.session.commit()
          result = {"id": persona_upd.id}
          
          return result
    except Exception as inst:
        message = {"result":"error"}
        logging.error(str(type(inst))+'\n Tipo de error: '+str(inst)+ '['+str(datetime.now())+']')
        return make_response(jsonify(message), 400)
