from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required

discharges = Blueprint("discharge", __name__, url_prefix="/api/v1/discharges")


@discharges.get("/<int:id>")
def read_one(id):
    return "Reading a discharges ... soon"


@discharges.post("/")
def create():
    return "Creating a discharges ... soon"


@discharges.put('/<int:id>')
@discharges.patch('/<int:id>')
def update(id):
    return "Updating a discharges ... soon"


@discharges.delete("/<int:id>")
def delete(id):
    return "Removing a discharges ... soon"

# Productos
@discharges.get("/<int:id>/products")
def read_products(id):
    return "Reading products of a discharges ... soon"

