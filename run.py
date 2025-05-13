from app import create_app
from app.views_volunteer import prueba1_bp
from app.views_shared_vehicle import prueba2_bp

app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ftc_parking:T3mp0ral#2025@10.3.11.203:3306/parking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

if __name__ == '__main__':
    print("   Acceso a formulario para voluntarios: http://127.0.0.1:5000/parking_access_volunteer")
    print("   Acceso a formulario para acceso con vehiculos compartidos: http://127.0.0.1:5000/parking_access_shared_vehicle\n")
    app.run(debug=True)

# Al ejecutar run.py, habres index.py:  http://127.0.0.1:5000/
# Para abrir parking_access_shared_vehicle: http://127.0.0.1:5000/parking_access_shared_vehicle
# Para abrir parking_access_volunteer: http://127.0.0.1:5000/parking_access_volunteer