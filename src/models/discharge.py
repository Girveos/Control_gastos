from datetime import datetime
from src.database import db , ma

class Discharge (db.Model):
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value       = db.Column(db.Float, nullable = False)
    date        = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(80), nullable=True)
    create_at   = db.Column(db.DateTime, default = datetime.now())
    update_at   = db.Column(db.DateTime, onupdate = datetime.now())
    user_id     = db.Column(db.String(10), db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Discharge >>> {self.name}"
    
    def as_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }
    
class DischargeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discharge
        include_fk = True
        
discharge_schema = DischargeSchema()
discharges_schema = DischargeSchema(many=True)
