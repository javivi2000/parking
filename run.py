from app import create_app
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
    print("   - Consultas: http://localhost:5000/conteo_multiple\n")
    app.run(debug=True)

"""
Archivo principal para ejecutar la aplicación Flask.

- Crea la app con create_app().
- Configura la conexión a la base de datos MySQL.
- Inicializa Flask-Migrate para gestionar migraciones de la base de datos.
- Al ejecutar, muestra URLs útiles y arranca el servidor en modo debug.
"""
