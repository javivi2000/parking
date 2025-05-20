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

    from .views_shared_vehicle import views_shared_vehicle_bp
    from .views_volunteer import views_volunteer_bp
    from .routes import routes

    # Registro de Blueprints
    app.register_blueprint(routes)
    app.register_blueprint(views_shared_vehicle_bp)
    app.register_blueprint(views_volunteer_bp)

    return app
