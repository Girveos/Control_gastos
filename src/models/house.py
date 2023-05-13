from datetime import datetime
from src.database import db , ma

class House(db.Model):
    registration        = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    address             = db.Column(db.String(50), nullable = False, unique = True)
    type                = db.Column(db.Integer, nullable = False)
    floor_count         = db.Column(db.Integer, nullable=True)
    user_id             = db.Column(db.String(10), db.ForeignKey('user.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    updated_at           = db.Column(db.DateTime, onupdate=datetime.now())
    created_at           = db.Column(db.DateTime, default=datetime.now())
   
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def _repr_(self) -> str:
        return f"House >>> {self.address}"
    
class HouseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = House
        include_fk = True 
        
house_schema = HouseSchema()
houses_schema = HouseSchema(many=True)
