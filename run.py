from app import create_app
from app.views_volunteer import views_volunteer_bp
from app.views_shared_vehicle import views_shared_vehicle_bp
from app import create_app, db
from flask_migrate import Migrate

app = create_app()

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ftc_parking:T3mp0ral#2025@10.3.11.203:3306/parking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    print("   - Visualizar Plazas Disponibles: http://127.0.0.1:5000/mapa")
    print("   - Acceso a formulario para voluntarios: http://127.0.0.1:5000/parking_access_volunteer")
    print("   - Acceso a formulario para acceso con vehículos compartidos: http://127.0.0.1:5000/parking_access_shared_vehicle")
    print("   - Consultas: http://localhost:5000/conteo_multiple\n")
    app.run(debug=True)


# Al ejecutar run.py, habres index.py:  http://127.0.0.1:5000/mapa
# Para abrir parking_access_shared_vehicle: http://127.0.0.1:5000/parking_access_shared_vehicle
# Para abrir parking_access_volunteer: http://127.0.0.1:5000/parking_access_volunteer

