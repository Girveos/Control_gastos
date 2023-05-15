from datetime import datetime
from src.database import db , ma

class Charge (db.Model):
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value       = db.Column(db.Float, nullable = False)
    date        = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(80), nullable=True)
    create_at   = db.Column(db.DateTime, default = datetime.now())
    update_at   = db.Column(db.DateTime, onupdate = datetime.now())
    user_id     = db.Column(db.String(10), db.ForeignKey('user.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Charge >>> {self.name}"
    
class ChargeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Charge
        include_fk = True
        
charge_schema = ChargeSchema()
charges_schema = ChargeSchema(many=True)
