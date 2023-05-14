from datetime import datetime
from src.database import db , ma
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.discharge import Discharge
from src.models.charge import Charge

class User(db.Model):
    id                      = db.Column(db.String(10), primary_key=True)
    name                    = db.Column(db.String(80), nullable = False)
    email                   = db.Column(db.String(60), unique = True, nullable = False)
    password                = db.Column(db.String(128), nullable=False)
    balance                 = db.Column(db.Float)
    create_at               = db.Column(db.DateTime, default = datetime.now())
    update_at               = db.Column(db.DateTime, onupdate = datetime.now())
    charges                 = db.relationship('Charge', backref='user', lazy=True)
    discharges              = db.relationship('Discharge', backref='user', lazy=True)

    charges = db.relationship('Charge', backref="owner")    
    discharges = db.relationship('Discharge', backref="owner")    
    
    def __init__(self, **fields):
        super().__init__(**fields)
        self.discharges = []
        self.charges = []
        
    def __repr__(self) -> str:
        return f"User >>> {self.name}"
    
    def __setattr__(self,name,value):
        if(name == "password"):
            value = User.hash_password(value)
            
        super(User, self).__setattr__(name, value)
        
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_balance(self):
        total_charges = sum(charge.value for charge in self.charges)
        total_discharges = sum(discharge.value for discharge in self.discharges)
        return total_charges - total_discharges
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = User
        include_fk = True
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)
