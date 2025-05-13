from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ==================================
# Modelo ParkingSpace (preexistente)
# ==================================
class ParkingSpace:
    def __init__(self, id):
        self.id = id
        self.occupied = False

    def occupy(self):
        self.occupied = True

    def free(self):
        self.occupied = False

# Lista de plazas de garaje, inicialmente todas libres (False = libre, True = ocupada)
NUM_PLAZAS = 77
plazas = [ParkingSpace(i) for i in range(NUM_PLAZAS)]


# ==================================
# Modelos nuevos
# ==================================

class Solicitud(db.Model):
    __tablename__ = 'solicitudes'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), nullable=False)
    tipo_plaza_id = db.Column(db.Integer, db.ForeignKey('tipo_plaza.id'), nullable=False)
    frecuencia_id = db.Column(db.Integer, db.ForeignKey('frecuencia.id'), nullable=False)
    ambito_id = db.Column(db.Integer, db.ForeignKey('ambito.id'), nullable=False)
    mifare = db.Column(db.Enum('si', 'no'), nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=db.func.current_timestamp())
    dias_franjas = db.relationship('SolicitudDiasFranja', backref='solicitud', cascade='all, delete-orphan')

class SolicitudDiasFranja(db.Model):
    __tablename__ = 'solicitud_dias_franjas'
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes.id'), nullable=False)
    dias_semana = db.Column(db.Enum('lunes_viernes', 'sabados_domingos', 'ambos'), nullable=False)
    franja_horaria_id = db.Column(db.Integer, db.ForeignKey('franja_horaria.id'), nullable=False)

class Solicitante(db.Model):
    __tablename__ = 'solicitantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    vehiculos = db.relationship('Vehiculo', backref='solicitante', cascade='all, delete-orphan')
    periodos_uso = db.relationship('PeriodoUso', backref='solicitante', cascade='all, delete-orphan')
    acompanantes = db.relationship('Acompanante', backref='solicitante', cascade='all, delete-orphan')

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), nullable=False)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)

class PeriodoUso(db.Model):
    __tablename__ = 'periodos_uso'
    id = db.Column(db.Integer, primary_key=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)
    periodo_inicio = db.Column(db.String(20), nullable=False)
    periodo_fin = db.Column(db.String(20), nullable=False)

class Acompanante(db.Model):
    __tablename__ = 'acompanantes'
    id = db.Column(db.Integer, primary_key=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)

