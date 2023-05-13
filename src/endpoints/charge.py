from flask import Blueprint

providers = Blueprint("providers", __name__, url_prefix="/api/v1/providers")

@providers.get("/")
def read_all():
    return "Reading al providers ... soon"


@providers.get("/<int:id>")
def read_one(id):
    return "Reading a providers ... soon"


@providers.post("/")
def create():
    return "Creating a providers ... soon"


@providers.put('/<int:id>')
@providers.patch('/<int:id>')
def update(id):
    return "Updating a providers ... soon"


@providers.delete("/<int:id>")
def delete(id):
    return "Removing a providers ... soon"

# Productos
@providers.get("/<int:id>/products")
def read_products(id):
    return "Reading products of a provider ... soon"

