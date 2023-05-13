from flask import Flask
from os import environ
from src.database import db, ma, migrate, jwt

from src.endpoints.users import users
from src.endpoints.auth import auth

def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)

    app.config['ENVIRONMENT'] = environ.get("ENVIRONMENT")
    config_class = 'config.DevelopmentConfig'

    match app.config['ENVIRONMENT']:
        case "development":
            config_class = 'config.DevelopmentConfig'
        case "production":
            config_class = 'config.ProductionConfig'
        case _:
            print(f"ERROR: environment unknown: {app.config.get('ENVIRONMENT')}")
            app.config['ENVIRONMENT'] = "development"
    app.config.from_object(config_class)
    
    app.register_blueprint(users)
    app.register_blueprint(auth)

    migrate.init_app(app,db)
    
    # Establish the database connection
    db.init_app(app)
    
    ## Create the data serializer
    ma.init_app(app)
    
    jwt.init_app(app)

    ## Create database tables
    with app.app_context():
        #db.drop_all()
        db.create_all()
    
    return app
