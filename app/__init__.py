# app/__init__.py
from flask import Flask
from .config import Config
from .models import db
import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'clave-secreta'
    app.config['SECRET_KEY'] = 'supersecreto123'

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)

<<<<<<< HEAD
    from .views_shared_vehicle import views_shared_vehicle_bp
    from .views_volunteer import views_volunteer_bp
    from .routes import routes

    # Registro de Blueprints
    app.register_blueprint(routes)
    app.register_blueprint(views_shared_vehicle_bp)
    app.register_blueprint(views_volunteer_bp)
=======
    from .routes import routes
    from .views import views_bp  

    # Registro de Blueprints
    app.register_blueprint(routes, url_prefix='')
    app.register_blueprint(views_bp, url_prefix='')
>>>>>>> 921a981 (Mejoras en la interfaz visual del parking)

    return app


"""
Este archivo inicializa la aplicación Flask y configura sus componentes principales.

- Importa Flask y otras configuraciones necesarias, incluyendo la configuración de la base de datos y los Blueprints.
- Usa pymysql para reemplazar el driver MySQLdb, facilitando la conexión a MySQL.
- Define la función create_app() que:
    * Crea una instancia de Flask.
    * Carga la configuración desde la clase Config.
    * Establece claves secretas para la sesión y seguridad.
    * Configura SQLAlchemy con la URI y opciones de seguimiento de cambios.
    * Inicializa la extensión de base de datos (SQLAlchemy) con la app.
    * Registra los Blueprints de rutas y vistas para modularizar la aplicación.
    * Devuelve la instancia de la aplicación Flask lista para usarse.
"""