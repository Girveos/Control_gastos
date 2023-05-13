from datetime import datetime
from src.database import db , ma

class Product (db.Model):
    #code           numerico, autoincremental, obligatorio, pk 
    #name           varhcar, unico, obligatorio
    #price          real, obligatorio
    #expiration     fecha, opcional
    #created_at     
    #updated_at     
    #user_id        FK user(id)
    code        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(50), nullable = False, unique = True)
    price       = db.Column(db.Float, nullable = False)
    expiration  = db.Column(db.Date, nullable=True)
    create_at   = db.Column(db.DateTime, default = datetime.now())
    update_at   = db.Column(db.DateTime, onupdate = datetime.now())
    user_id     = db.Column(db.String(10), db.ForeignKey('user.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Prodcut >>> {self.name}"
    
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = Product
        include_fk = True
        
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
