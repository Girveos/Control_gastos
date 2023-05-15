from datetime import datetime
from sqlalchemy.orm import validates
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
    
    @validates('date')
    def validate_date(self, key, date):
        if isinstance(date, datetime):
            return date
        try:
            datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return date
        except ValueError:
            raise ValueError('The time format is invalid. Use the format "year-month-day hour:minute:second".')
    
    @validates('value')
    def validate_observations(self, key, value):
        if not value:
            raise AssertionError('No value provided')
        if value < 0:
            raise AssertionError('Value must be positive')
        return value
    
class DischargeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discharge
        include_fk = True
        
discharge_schema = DischargeSchema()
discharges_schema = DischargeSchema(many=True)
