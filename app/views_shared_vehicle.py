from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Solicitante, Vehiculo, PeriodoUso, Acompanante
from datetime import datetime

# Definición del Blueprint
views_shared_vehicle_bp = Blueprint('views_shared_vehicle', __name__, template_folder='templates')

# Ruta para mostrar el formulario
@views_shared_vehicle_bp.route('/parking_access_shared_vehicle', methods=['GET'])
def index():
    return render_template('parking_access_shared_vehicle.html')

# Ruta para procesar el formulario
@views_shared_vehicle_bp.route('/parking_access_shared_vehicle/guardar', methods=['POST'])
def guardar():
    try:
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        matricula = request.form['matricula']
        periodo_ini = request.form['periodoini']
        periodo_fin = request.form['periodofin']
        acompanante1 = request.form['acompanante1']
        acompanante2 = request.form['acompanante2']
        acompanante3 = request.form['acompanante3']

        # Crear nuevo solicitante
        solicitante = Solicitante(
            nombre=nombre,
            telefono=telefono,
            correo=f'{nombre.split()[0].lower()}@example.com'  # Generar correo con el primer nombre
        )
        db.session.add(solicitante)
        db.session.commit()

        # Crear nuevo vehículo
        vehiculo = Vehiculo(
            matricula=matricula,
            solicitante_id=solicitante.id
        )
        db.session.add(vehiculo)

        # Crear el periodo de uso
        periodo_uso = PeriodoUso(
            solicitante_id=solicitante.id,
            periodo_inicio=periodo_ini,
            periodo_fin=periodo_fin
        )
        db.session.add(periodo_uso)

        # Agregar acompañantes si existen
        if acompanante1:
            db.session.add(Acompanante(solicitante_id=solicitante.id, nombre=acompanante1, numero=1))
        if acompanante2:
            db.session.add(Acompanante(solicitante_id=solicitante.id, nombre=acompanante2, numero=2))
        if acompanante3:
            db.session.add(Acompanante(solicitante_id=solicitante.id, nombre=acompanante3, numero=3))

        # Validar que la fecha de inicio no sea posterior a la de fin
        inicio = datetime.strptime(periodo_ini, "%Y-%m-%d")
        fin = datetime.strptime(periodo_fin, "%Y-%m-%d")
        if inicio > fin:
            flash("La fecha de inicio no puede ser posterior a la de fin", "danger")
            return redirect(url_for('views_shared_vehicle.index'))

        # Confirmar la transacción
        db.session.commit()

        flash('El formulario enviado con éxito', 'success')
        return redirect(url_for('views_shared_vehicle.index'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar los datos: {str(e)}', 'danger')
        return redirect(url_for('views_shared_vehicle.index'))
