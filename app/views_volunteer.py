from flask import Blueprint, render_template, request, jsonify
from app.models import db, Solicitante, Vehiculo, PeriodoUso, Acompanante
from datetime import datetime

# Definición del Blueprint
prueba1_bp = Blueprint('views_volunteer', __name__, template_folder='templates')

# Ruta para mostrar el formulario
@prueba1_bp.route('/parking_access_volunteer', methods=['GET'])
def index():
    return render_template('parking_access_volunteer.html')

# Ruta para procesar el formulario
@prueba1_bp.route('/parking_access_volunteer/guardar', methods=['POST'])
def guardar():
    try:
        # Obtener los datos del formulario
        apellidos_nombre = request.form.get('apellidos_nombre')
        dni = request.form.get('dni')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        ambito = request.form.get('ambito')
        frecuencia = request.form.get('frecuencia')
        tipo_plaza = request.form.get('tipo_plaza')
        dias_semana = request.form.get('dias_semana')
        franja_horaria_id = request.form.get('franja_horaria_id')
        mifare = request.form.get('mifare')

        # Crear nuevo solicitante
        solicitante = Solicitante(
            nombre=apellidos_nombre,
            telefono=telefono,
            correo=correo
        )
        db.session.add(solicitante)
        db.session.commit()

        # Crear el periodo de uso
        periodo_uso = PeriodoUso(
            solicitante_id=solicitante.id,
            periodo_inicio='2025-05-14',
            periodo_fin='2025-05-15'
        )
        db.session.add(periodo_uso)
        db.session.commit()

        # Respuesta JSON de éxito incluyendo los datos enviados
        return jsonify({
            'success': True,
            'data': {
                'apellidos_nombre': apellidos_nombre,
                'dni': dni,
                'telefono': telefono,
                'correo': correo,
                'ambito': ambito,
                'frecuencia': frecuencia,
                'tipo_plaza': tipo_plaza,
                'dias_semana': dias_semana,
                'franja_horaria_id': franja_horaria_id,
                'mifare': mifare
            }
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar: {str(e)}")  # Agregar un print para ver el error en consola
        return jsonify({'success': False, 'error': str(e)})
