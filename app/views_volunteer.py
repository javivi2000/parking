from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Solicitud, SolicitudDiasFranja

prueba1_bp = Blueprint('views_volunteer', __name__, template_folder='templates')

@prueba1_bp.route('/parking_access_volunteer', methods=['GET'])
def index():
    return render_template('parking_access_volunteer.html')

@prueba1_bp.route('/parking_access_volunteer/guardar', methods=['POST'])
def guardar():
    try:
        correo = request.form['email']
        ambito_id = request.form['ambito_id']
        frecuencia_id = request.form['frecuencia_id']
        tipo_plaza_id = request.form['tipo_plaza_id']
        mifare = request.form['mifare']
        dias_semana = request.form['dias_semana']
        franja_horaria_id = request.form['franja_horaria_id']

        solicitud = Solicitud(
            correo=correo,
            ambito_id=ambito_id,
            frecuencia_id=frecuencia_id,
            tipo_plaza_id=tipo_plaza_id,
            mifare=mifare
        )
        db.session.add(solicitud)
        db.session.commit()

        solicitud_dia_franja = SolicitudDiasFranja(
            solicitud_id=solicitud.id,
            dias_semana=dias_semana,
            franja_horaria_id=franja_horaria_id
        )
        db.session.add(solicitud_dia_franja)
        db.session.commit()

        flash('El formulario enviado con éxito', 'success')
        return redirect(url_for('views_volunteer.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar los datos: {str(e)}', 'danger')
        return redirect(url_for('views_volunteer.index'))
