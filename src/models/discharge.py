from datetime import datetime
from src.database import db , ma

class Discharge (db.Model):
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value       = db.Column(db.Float, nullable = False)
    date        = db.Column(db.Date, nullable=True)
    description = db.Column(db.String(80), nullable=True)
    create_at   = db.Column(db.DateTime, default = datetime.now())
    update_at   = db.Column(db.DateTime, onupdate = datetime.now())
    user_id     = db.Column(db.String(10), db.ForeignKey('user.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Discharge >>> {self.name}"
    
class DischargeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = Discharge
        include_fk = True
        
discharge_schema = DischargeSchema()
discharges_schema = DischargeSchema(many=True)
