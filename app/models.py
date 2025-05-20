from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import Flask

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

NUM_PLAZAS = 77
plazas = [ParkingSpace(i) for i in range(NUM_PLAZAS)]


# ==================================
# Modelos nuevos ajustados
# ==================================

class Solicitante(db.Model):
    __tablename__ = 'solicitantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    dni = db.Column(db.String(50), nullable=True)
    fecha_registro = db.Column(db.TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    vehiculos = db.relationship('Vehiculo', backref='solicitante', cascade='all, delete-orphan')
    periodos_uso = db.relationship('PeriodoUso', backref='solicitante', cascade='all, delete-orphan')
    acompanantes = db.relationship('Acompanante', backref='solicitante', cascade='all, delete-orphan')
    solicitudes = db.relationship('Solicitud', backref='solicitante', cascade='all, delete-orphan')


class Solicitud(db.Model):
    __tablename__ = 'solicitudes'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), nullable=False)
    ambito_id = db.Column(db.Integer, db.ForeignKey('ambito.id'), nullable=False)
    frecuencia_id = db.Column(db.Integer, db.ForeignKey('frecuencia.id'), nullable=False)
    tipo_plaza_id = db.Column(db.Integer, db.ForeignKey('tipo_plaza.id'), nullable=False)
    mifare = db.Column(db.Enum('si', 'no', name='mifare_enum'), nullable=False)
    fecha_solicitud = db.Column(db.TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)

    ambito = db.relationship('Ambito')
    frecuencia = db.relationship('Frecuencia')
    tipo_plaza = db.relationship('TipoPlaza')
    dias_franjas = db.relationship('SolicitudDiasFranja', backref='solicitud_asociada', cascade='all, delete-orphan')  # Cambié el backref a 'solicitud_asociada'


class SolicitudDiasFranja(db.Model):
    __tablename__ = 'solicitud_dias_franjas'

    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes.id'), nullable=False)
    dias_semana = db.Column(db.Enum('lunes_viernes', 'sabados_domingos', 'ambos', name='dias_semana_enum'), nullable=False)
    franja_horaria_id = db.Column(db.Integer, db.ForeignKey('franja_horaria.id'), nullable=False)

    franja_horaria = db.relationship('FranjaHoraria')


class TipoPlaza(db.Model):
    __tablename__ = 'tipo_plaza'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)


class Frecuencia(db.Model):
    __tablename__ = 'frecuencia'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)


class Ambito(db.Model):
    __tablename__ = 'ambito'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)


class FranjaHoraria(db.Model):
    __tablename__ = 'franja_horaria'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)


# ==================================
# Modelos para vehículo compartido
# ==================================

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'

    id = db.Column(db.Integer, primary_key=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)
    matricula = db.Column(db.String(20), nullable=False)


class PeriodoUso(db.Model):
    __tablename__ = 'periodos_uso'

    id = db.Column(db.Integer, primary_key=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)
    periodo_inicio = db.Column(db.Date, nullable=False)
    periodo_fin = db.Column(db.Date, nullable=False)


class Acompanante(db.Model):
    __tablename__ = 'acompanantes'

    id = db.Column(db.Integer, primary_key=True)
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitantes.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
