from flask import Blueprint, request
from http import HTTPStatus
from src.database import db
import werkzeug 
import sqlalchemy.exc
from datetime import datetime


from src.models.discharge import Discharge, discharge_schema, discharges_schema

discharges = Blueprint("discharge", __name__, url_prefix="/api/v1/discharges")

@discharges.get("/user/<int:user_id>")
def read_one(user_id):
    discharges = Discharge.query.filter_by(user_id=user_id).all()
    if not discharges:
        return {"message": "No discharges found for this user"}, HTTPStatus.NOT_FOUND
    
    return {"data":  discharges_schema.dump(discharges)}, HTTPStatus.OK



@discharges.post("/")
def create():
    # Obtener los datos del discharge del cuerpo de la solicitud
    data = request.get_json()
    
    # Crear una nueva instancia de la clase Discharge con los datos proporcionados
    discharge = Discharge(
                value = request.get_json().get("value", None),
                date = datetime.fromisoformat(request.get_json().get("date", None)),
                description = request.get_json().get("description", None),
                user_id = request.get_json().get("user_id", None),
    )

    # Agregar el nuevo discharge a la base de datos
    db.session.add(discharge)
    db.session.commit()

    # Devolver una respuesta al cliente con el nuevo discharge creado y el código de estado HTTP 201 Created
    return {'data': discharge_schema.dump(discharge)}, HTTPStatus.CREATED



@discharges.put('/<int:id>')
def update_discharges(id):
    post_data = None
    
    try:
        post_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    discharge = Discharge.query.filter_by(id=id).first()
    
    if(not discharge):
        return {"error": "resource not found"}, HTTPStatus.NOT_FOUND
            
    discharge.value = request.get_json().get("value", discharge.value)
    discharge.date = datetime.fromisoformat(request.get_json().get("date", discharge.date))
    discharge.description = request.get_json().get("description", discharge.description)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data":discharge_schema.dump(discharge)}, HTTPStatus.OK


@discharges.delete("/<int:id>")
def delete(id):   
    discharge = Discharge.query.filter_by(id=id).first()
    
    if(not discharge):
        return {"error": "resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(discharge)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data":""}, HTTPStatus.NO_CONTENT
 

