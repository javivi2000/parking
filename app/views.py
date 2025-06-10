#views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import db, Solicitante, Vehiculo, PeriodoUso, Acompanante, Solicitud, SolicitudDiasFranja, Ambito
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


# Definición del Blueprint único
views_bp = Blueprint('views', __name__, template_folder='templates')

# --- RUTAS PARA VEHÍCULOS COMPARTIDOS ---

@views_bp.route('/parking_access_shared_vehicle', methods=['GET'])
def shared_vehicle_index():
    return render_template('parking_access_shared_vehicle.html')

@views_bp.route('/parking_access_shared_vehicle/guardar', methods=['POST'])
def shared_vehicle_guardar():
    try:
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        matricula = request.form['matricula']
        periodo_ini = request.form['periodoini']
        periodo_fin = request.form['periodofin']
        acompanante1 = request.form.get('acompanante1', '')
        acompanante2 = request.form.get('acompanante2', '')
        acompanante3 = request.form.get('acompanante3', '')

        # Validar fechas
        inicio = datetime.strptime(periodo_ini, "%Y-%m-%d")
        fin = datetime.strptime(periodo_fin, "%Y-%m-%d")
        if inicio > fin:
            flash("La fecha de inicio no puede ser posterior a la de fin", "danger")
            return redirect(url_for('views.shared_vehicle_index'))

        # Crear nuevo solicitante
        solicitante = Solicitante(
            nombre=nombre,
            telefono=telefono,
            correo=f'{nombre.split()[0].lower()}@example.com'
        )
        db.session.add(solicitante)
        db.session.commit()  # Para obtener solicitante.id

        # Crear vehículo
        vehiculo = Vehiculo(
            matricula=matricula,
            solicitante_id=solicitante.id
        )
        db.session.add(vehiculo)

        # Crear periodo de uso
        periodo_uso = PeriodoUso(
            solicitante_id=solicitante.id,
            periodo_inicio=periodo_ini,
            periodo_fin=periodo_fin
        )
        db.session.add(periodo_uso)

        # Acompañantes
        if acompanante1:
            db.session.add(Acompanante(solicitante_id=solicitante.id, nombre=acompanante1, numero=1))
        if acompanante2:
            db.session.add(Acompanante(solicitante_id=solicitante.id, nombre=acompanante2, numero=2))
        if acompanante3:
            db.session.add(Acompanante(solicitante_id=solicitante.id, nombre=acompanante3, numero=3))

        db.session.commit()

        flash('El formulario enviado con éxito', 'success')
        return redirect(url_for('views.shared_vehicle_index'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar los datos: {str(e)}', 'danger')
        return redirect(url_for('views.shared_vehicle_index'))


# --- RUTAS PARA VOLUNTARIADO ---

@views_bp.route('/parking_access_volunteer', methods=['GET'])
def volunteer_index():
    return render_template('parking_access_volunteer.html')

@views_bp.route('/parking_access_volunteer/guardar', methods=['POST'])
def volunteer_guardar():
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

        # Validar ámbito
        ambito_obj = Ambito.query.get(int(ambito))
        if not ambito_obj:
            return f'El ámbito con ID {ambito} no existe.', 400

        # Buscar o crear solicitante
        solicitante = Solicitante.query.filter_by(correo=correo).first()
        if not solicitante:
            solicitante = Solicitante(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                dni=dni
            )
            db.session.add(solicitante)
            db.session.flush()  # Para obtener solicitante.id sin commit aún

        # Crear solicitud
        solicitud = Solicitud(
            solicitante_id=solicitante.id,
            correo=correo,
            ambito_id=int(ambito),
            frecuencia_id=int(frecuencia),
            tipo_plaza_id=int(tipo_plaza),
            mifare='si' if mifare == 'si' else 'no'
        )
        db.session.add(solicitud)
        db.session.flush()

        # Crear días y franja horaria
        solicitud_dia_franja = SolicitudDiasFranja(
            solicitud_id=solicitud.id,
            dias_semana=dias_semana,
            franja_horaria_id=int(franja_horaria)
        )
        db.session.add(solicitud_dia_franja)

        db.session.commit()

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

"""
Definición del Blueprint 'views_bp' que agrupa las rutas relacionadas con la gestión
de formularios y operaciones para vehículos compartidos y voluntariado.

- Ruta '/parking_access_shared_vehicle' (GET):
  Renderiza la plantilla para el formulario de acceso de vehículos compartidos.

- Ruta '/parking_access_shared_vehicle/guardar' (POST):
  Recibe los datos del formulario de vehículo compartido.
  Valida fechas, crea un nuevo solicitante, vehículo, periodos de uso y acompañantes.
  Guarda todo en la base de datos con manejo de errores y muestra mensajes flash para el usuario.

- Ruta '/parking_access_volunteer' (GET):
  Renderiza la plantilla para el formulario de acceso de voluntariado.

- Ruta '/parking_access_volunteer/guardar' (POST):
  Recibe datos del formulario de voluntariado.
  Valida campos obligatorios y existencia del ámbito.
  Busca o crea un solicitante.
  Crea una solicitud y sus días/franjas horarios relacionados.
  Guarda en base de datos con manejo de errores.
  Devuelve JSON con los datos ingresados o mensaje de error.

El archivo maneja la lógica de negocio para la recepción, validación, almacenamiento y retroalimentación
de formularios de usuarios relacionados con plazas de aparcamiento para vehículos compartidos y voluntarios.
"""
