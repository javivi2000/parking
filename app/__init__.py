from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .models import db
from .views_shared_vehicle import prueba2_bp
from .views_volunteer import prueba1_bp
from .routes import routes  
import pymysql
pymysql.install_as_MySQLdb()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'clave-secreta'  

    # Configuración de la base de datos 
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)

    # Registro de Blueprints
    app.register_blueprint(routes)        
    app.register_blueprint(prueba2_bp)
    app.register_blueprint(prueba1_bp)

    return app
