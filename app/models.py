from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data.excel_utils import cargar_plazas, cargar_solicitudes, cargar_tipos_plaza
from sqlalchemy import func
import pandas as pd

db = SQLAlchemy()

# ==================================
# Modelos existentes
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

class Ambito(db.Model):
    __tablename__ = 'ambito'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

class Frecuencia(db.Model):
    __tablename__ = 'frecuencia'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

class FranjaHoraria(db.Model):
    __tablename__ = 'franja_horaria'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

class TipoPlaza(db.Model):
    __tablename__ = 'tipo_plaza'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)

class Plaza(db.Model):
    __tablename__ = 'plaza'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.String(255))
    ultima_ocupacion = db.Column(db.DateTime, nullable=True)
    tipo_plaza_id = db.Column(db.Integer, db.ForeignKey('tipo_plaza.id'), nullable=True)
    tipo_plaza = db.relationship('TipoPlaza', backref='plazas')
    historial_ocupaciones = db.relationship(
        'HistorialOcupacion', back_populates='plaza', cascade='all, delete-orphan'
    )

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
    plaza_id = db.Column(db.Integer, db.ForeignKey('plaza.id'), nullable=True)

    ambito = db.relationship('Ambito')
    frecuencia = db.relationship('Frecuencia')
    tipo_plaza = db.relationship('TipoPlaza')
    plaza = db.relationship('Plaza')
    dias_franjas = db.relationship('SolicitudDiasFranja', backref='solicitud_asociada', cascade='all, delete-orphan')

class SolicitudDiasFranja(db.Model):
    __tablename__ = 'solicitud_dias_franjas'
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes.id'), nullable=False)
    dias_semana = db.Column(db.Enum('lunes_viernes', 'sabados_domingos', 'ambos', name='dias_semana_enum'), nullable=False)
    franja_horaria_id = db.Column(db.Integer, db.ForeignKey('franja_horaria.id'), nullable=False)

    franja_horaria = db.relationship('FranjaHoraria')

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


class HistorialOcupacion(db.Model):
    __tablename__ = 'historial_ocupacion'
    id = db.Column(db.Integer, primary_key=True)
    plaza_id = db.Column(db.Integer, db.ForeignKey('plaza.id'))
    tipo_plaza_id = db.Column(db.Integer, db.ForeignKey('tipo_plaza.id')) 
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.DateTime, nullable=False)
    hora_fin = db.Column(db.DateTime, nullable=True)

    plaza = db.relationship('Plaza', back_populates='historial_ocupaciones')
    tipo_plaza = db.relationship('TipoPlaza')

class RegistroClickPlaza(db.Model):
    __tablename__ = 'registro_click_plaza'
    id = db.Column(db.Integer, primary_key=True)
    plaza_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ===========================
# FUNCIONES PARA DATOS DE EXCEL
# ===========================

# Rutas a los excels
EXCEL_PLAZAS = 'data/Plazas Movilidad y Voluntariado.xlsx'
EXCEL_SOLICITUDES = 'data/Vehículos compartidos.xlsx'

def cargar_plazas():
    """Devuelve una lista de dicts con los datos de las plazas desde el Excel."""
    df = pd.read_excel(EXCEL_PLAZAS)
    # Buscar el nombre real de la columna ID (insensible a mayúsculas)
    id_col = next((col for col in df.columns if col.strip().lower() in ['id', 'plaza id']), None)
    tipo_col = next((col for col in df.columns if col.strip().lower() in ['tipo plaza', 'tipo_plaza_id']), None)
    estado_col = next((col for col in df.columns if col.strip().lower() in ['ocupada', 'estado']), None)
    ultima_col = next((col for col in df.columns if 'ultima' in col.strip().lower()), None)

    plazas = []
    for _, row in df.iterrows():
        plazas.append({
            'id': int(row[id_col]) if id_col and not pd.isnull(row[id_col]) else None,
            'tipo': row.get(tipo_col) if tipo_col else None,
            'estado': bool(row.get(estado_col, False)) if estado_col else False,
            'ultima_ocupacion': row.get(ultima_col, None) if ultima_col else None
        })
    return plazas

def cargar_solicitudes():
    """Devuelve una lista de dicts con los datos de las solicitudes desde el Excel."""
    df = pd.read_excel(EXCEL_SOLICITUDES)
    solicitudes = []
    for _, row in df.iterrows():
        solicitudes.append({
            'id': int(row['ID']) if not pd.isnull(row['ID']) else None,
            'solicitante_id': int(row.get('Solicitante ID')) if not pd.isnull(row.get('Solicitante ID')) else None,
            'tipo_plaza_id': row.get('Tipo Plaza') or row.get('tipo_plaza_id'),
            'plaza_id': int(row.get('Plaza ID')) if not pd.isnull(row.get('Plaza ID')) else None,
            'correo': row.get('Correo', ''),
            'fecha': row.get('Fecha', ''),
        })
    return solicitudes

def cargar_solicitantes():
    """Devuelve una lista de dicts con los datos de los solicitantes desde el Excel de solicitudes."""
    df = pd.read_excel(EXCEL_SOLICITUDES)
    solicitantes = []
    for _, row in df.iterrows():
        solicitantes.append({
            'id': int(row.get('Solicitante ID')) if not pd.isnull(row.get('Solicitante ID')) else None,
            'nombre': row.get('Solicitante', ''),
            'correo': row.get('Correo', ''),
        })
    return solicitantes

def cargar_tipos_plaza():
    """Devuelve los tipos de plaza únicos desde el Excel de plazas."""
    df = pd.read_excel(EXCEL_PLAZAS)
    return df['Tipo Plaza'].dropna().unique().tolist() if 'Tipo Plaza' in df else []

def get_solicitudes_por_tipo(tipo_plaza):
    """Devuelve las solicitudes filtradas por tipo de plaza."""
    solicitudes = cargar_solicitudes()
    return [s for s in solicitudes if s['tipo_plaza_id'] == tipo_plaza]

def get_plazas_libres(tipo=None):
    """Devuelve las plazas libres, opcionalmente filtradas por tipo."""
    plazas = cargar_plazas()
    libres = [p for p in plazas if not p['estado']]
    if tipo:
        libres = [p for p in libres if p['tipo'] == tipo]
    return libres

def get_plaza_by_id(plaza_id):
    """Devuelve una plaza por su ID."""
    plazas = cargar_plazas()
    for plaza in plazas:
        if plaza['id'] == plaza_id:
            return plaza
    return None

def get_solicitante_by_id(solicitante_id):
    """Devuelve un solicitante por su ID."""
    solicitantes = cargar_solicitantes()
    for s in solicitantes:
        if s['id'] == solicitante_id:
            return s
    return None

def get_solicitudes_by_solicitante(solicitante_id):
    """Devuelve todas las solicitudes de un solicitante."""
    solicitudes = cargar_solicitudes()
    return [s for s in solicitudes if s['solicitante_id'] == solicitante_id]


"""
Este archivo:

- Define todos los modelos de base de datos para solicitudes, plazas y usuarios.

- Carga datos desde archivos Excel.

- Proporciona funciones para consultar y manipular estos datos.

- Incluye una clase ParkingSpace que simula ocupación de plazas para el mapa visual de la app.
"""