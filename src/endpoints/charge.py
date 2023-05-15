from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from src.database import db
import werkzeug 
import sqlalchemy.exc
from datetime import datetime


from src.models.charge import Charge, charge_schema, charges_schema

charges = Blueprint("charge", __name__, url_prefix="/api/v1/charges")

@jwt_required()
@charges.get("/user/<int:user_id>")
def read_one(user_id):
    charges = Charge.query.filter_by(user_id=user_id).all()
    if not charges:
        return {"message": "No charges found for this user"}, HTTPStatus.NOT_FOUND
    
    return {"data":  charges_schema.dump(charges)}, HTTPStatus.OK



@charges.post("/")
def create():
    # Obtener los datos del charge del cuerpo de la solicitud
    data = request.get_json()
    
    # Crear una nueva instancia de la clase charge con los datos proporcionados
    charge = Charge(
                value = request.get_json().get("value", None),
                date = datetime.fromisoformat(request.get_json().get("date", None)),
                description = request.get_json().get("description", None),
                user_id = request.get_json().get("user_id", None),
    )

    # Agregar el nuevo charge a la base de datos
    db.session.add(charge)
    db.session.commit()

    # Devolver una respuesta al cliente con el nuevo charge creado y el código de estado HTTP 201 Created
    return {'data': charge_schema.dump(charge)}, HTTPStatus.CREATED


@jwt_required()
@charges.put('/<int:id>')
def update_charges(id):
    post_data = None
    
    try:
        post_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    charge = Charge.query.filter_by(id=id).first()
    
    if(not charge):
        return {"error": "resource not found"}, HTTPStatus.NOT_FOUND
            
    charge.value = request.get_json().get("value", charge.value)
    charge.date = datetime.fromisoformat(request.get_json().get("date", charge.date))
    charge.description = request.get_json().get("description", charge.description)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data":charge_schema.dump(charge)}, HTTPStatus.OK


@charges.delete("/<int:id>")
def delete(id):   
    charge = Charge.query.filter_by(id=id).first()
    
    if(not charge):
        return {"error": "resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(charge)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data":""}, HTTPStatus.NO_CONTENT
 
