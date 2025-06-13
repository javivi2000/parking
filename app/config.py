import os

class Config:
    SECRET_KEY = 'clave-secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ftc_parking:T3mp0ral#2025@10.3.11.203:3306/parking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

"""
Este archivo define la configuración de una app Flask:

- Establece una clave secreta (SECRET_KEY) para seguridad.

- Configura la conexión a la base de datos MySQL con SQLAlchemy.

- Desactiva el seguimiento de cambios innecesarios para mejorar el rendimiento.
"""