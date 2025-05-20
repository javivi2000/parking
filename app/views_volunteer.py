from flask import Blueprint, render_template, request, jsonify
from app.models import db, Solicitante, Solicitud, SolicitudDiasFranja, Ambito  # Importa el modelo Ambito
from sqlalchemy.exc import SQLAlchemyError

views_volunteer_bp = Blueprint('views_volunteer', __name__, template_folder='templates')

@views_volunteer_bp.route('/parking_access_volunteer', methods=['GET'])
def index():
    return render_template('parking_access_volunteer.html')

@views_volunteer_bp.route('/parking_access_volunteer/guardar', methods=['POST'])
def guardar():
    try:
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        dni = request.form['dni']
        ambito = request.form['ambito']
        frecuencia = request.form['frecuencia']
        tipo_plaza = request.form['tipo_plaza']
        dias_semana = request.form['dias_semana']
        franja_horaria = request.form['franja_horaria']
        mifare = request.form.get('mifare', 'no')

        # Validación básica
        if not nombre or not correo or not dni or not telefono:
            return 'Faltan campos obligatorios.', 400

        # Validar que el ámbito exista
        ambito_obj = Ambito.query.get(int(ambito))
        if not ambito_obj:
            return f'El ámbito con ID {ambito} no existe.', 400

        # Buscar o crear el solicitante
        solicitante = Solicitante.query.filter_by(correo=correo).first()
        if not solicitante:
            solicitante = Solicitante(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                dni=dni
            )
            db.session.add(solicitante)
            db.session.flush()

        # Crear solicitud
        solicitud = Solicitud(
            solicitante_id=solicitante.id,
            correo=correo,  # Agregado para evitar que sea NULL
            ambito_id=int(ambito),
            frecuencia_id=int(frecuencia),
            tipo_plaza_id=int(tipo_plaza),
            mifare='si' if mifare == 'si' else 'no'
        )
        db.session.add(solicitud)
        db.session.flush()

        # Días y franja horaria
        solicitud_dia_franja = SolicitudDiasFranja(
            solicitud_id=solicitud.id,
            dias_semana=dias_semana,
            franja_horaria_id=int(franja_horaria)
        )
        db.session.add(solicitud_dia_franja)

        db.session.commit()

        # Enviar respuesta JSON que espera el frontend
        return jsonify({
            'nombre': nombre,
            'dni': dni,
            'telefono': telefono,
            'correo': correo,
            'ambito': ambito,
            'frecuencia': frecuencia,
            'tipoPlaza': tipo_plaza,
            'diasSemana': dias_semana,
            'franjaHoraria': franja_horaria,
            'mifare': mifare
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return f'Error al guardar en base de datos: {str(e)}', 500
    except Exception as e:
        db.session.rollback()
        return f'Error inesperado: {str(e)}', 500
