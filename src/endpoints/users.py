from flask import Blueprint, request, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required
import werkzeug 
import sqlalchemy.exc
from src.database import db

from src.models.user import User, user_schema, users_schema
from src.models.charge import Charge, charge_schema
from src.models.discharge import Discharge, discharge_schema

users = Blueprint("users", __name__, url_prefix="/api/v1/users")

@jwt_required()
@users.get("/<string:id>")
def read_one(id):
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": user_schema.dump(user)},HTTPStatus.OK

@users.post("/")
def create():
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {
            "error": "Post body JSON data not found",
            "message": str(e)
        }, HTTPStatus.BAD_REQUEST

    user = User(
        id=request.get_json().get("id", None),
        name=request.get_json().get("name", None),
        email=request.get_json().get("email", None),
        password=request.get_json().get("password", None),
    )

    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {
            "error": "Invalid resource values",
            "message": str(e)
        }, HTTPStatus.BAD_REQUEST

    return {"data": user_schema.dump(user)}, HTTPStatus.CREATED

@jwt_required()
@users.put("/<int:id>")
def update_user(id):
    post_data = None

    try:
        post_data = request.get_json()

    except werkzeug.exceptions.BadRequest as e:
        return {
            "error": "Put body JSON data not found",
            "message": str(e)
        }, HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(id=id).first()

    if (not user):
        return {"error": "resource not found"}, HTTPStatus.NOT_FOUND

    user.name = request.get_json().get("name", user.name)
    user.email = request.get_json().get("email", user.email)
    user.password = request.get_json().get("password", user.password)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {
            "error": "Invalid resource values",
            "message": str(e)
        }, HTTPStatus.BAD_REQUEST

    return {"data": user_schema.dump(user)}, HTTPStatus.OK


@users.delete("/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()

    if (not user):
        return {"error": "resource not found"}, HTTPStatus.NOT_FOUND

    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {
            "error": "Resource could not be deleted",
            "message": str(e)
        }, HTTPStatus.BAD_REQUEST

    return {"data": ""}, HTTPStatus.NO_CONTENT


@users.route('/<int:id>/balance')
def get_user_balance(id):
    user = User.query.get_or_404(id)
    balance = user.get_balance()
    return {"balance": balance}


@users.route('/<int:id>/discharges', methods=['GET'])
def get_user_dischagres(id):
    user = User.query.get_or_404(id)
    egresos = user.get_discharges_on_range(request.get_json().get("fecha_inicio"),request.get_json().get("fecha_fin"))
    return jsonify([egreso.as_dict() for egreso in egresos])

@users.route('/<int:id>/charges', methods=['GET'])
def get_user_chagres(id):
    user = User.query.get_or_404(id)
    ingresos = user.get_charges_on_range(request.get_json().get("fecha_inicio"),request.get_json().get("fecha_fin"))
    return jsonify([ingreso.as_dict() for ingreso in ingresos])


@users.get("/<int:id>/transactions")
def read_user_transactions(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    # Obtener todas las transacciones del usuario
    transactions = []
    for charge in user.charges:
        transactions.append({"id": charge.id, "value": charge.value, "date": charge.date, "type": "charge"})
    for discharge in user.discharges:
        transactions.append({"id": discharge.id, "value": discharge.value, "date": discharge.date, "type": "discharge"})

    # Ordenar las transacciones por fecha descendente
    transactions = sorted(transactions, key=lambda t: t["date"], reverse=True)

    return {"data": transactions}, HTTPStatus.OK


