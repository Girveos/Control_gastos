from datetime import datetime
import re
from flask import jsonify
from sqlalchemy.orm import validates
from src.database import db , ma
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.discharge import Discharge
from src.models.charge import Charge

class User(db.Model):
    id                      = db.Column(db.String(10), primary_key=True)
    name                    = db.Column(db.String(80), nullable = False)
    email                   = db.Column(db.String(60), unique = True, nullable = False)
    password                = db.Column(db.String(128), nullable=False)
    balance                 = db.Column(db.Float, default=0)
    create_at               = db.Column(db.DateTime, default = datetime.now())
    update_at               = db.Column(db.DateTime, onupdate = datetime.now())
    charges                 = db.relationship('Charge', backref='user', lazy=True)
    discharges              = db.relationship('Discharge', backref='user', lazy=True)  
    
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
        
    
    @validates('code')
    def validate_code(self, key, value):
        if not value:
            raise AssertionError('No code provided')
        if User.query.filter(User.id == value).first():
            raise AssertionError('Id is already in use')
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise AssertionError('No email provided')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError('The email format is invalid')
        if User.query.filter(User.email == value).first():
            raise AssertionError('email is already in use')
        return value
    
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_balance(self):
        total_charges = sum(charge.value for charge in self.charges)
        total_discharges = sum(discharge.value for discharge in self.discharges)
        return total_charges - total_discharges
    
    def get_discharges_on_range(self, fecha_inicio, fecha_fin):
        # Convertir las fechas a objetos de tipo datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        # Realizar la consulta utilizando la relación de la tabla Egreso
        egresos = Discharge.query.filter(and_(Discharge.user_id == self.id,
                                            Discharge.date >= fecha_inicio,
                                            Discharge.date <= fecha_fin)).all()
        return egresos
    
    def get_charges_on_range(self, fecha_inicio, fecha_fin):
        # Convertir las fechas a objetos de tipo datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        # Realizar la consulta utilizando la relación de la tabla Egreso
        ingresos = Charge.query.filter(and_(Charge.user_id == self.id,
                                            Charge.date >= fecha_inicio,
                                            Charge.date <= fecha_fin)).all()
        return ingresos
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields = ()
        model = User
        include_fk = True
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)
