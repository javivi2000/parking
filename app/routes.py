from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models import Solicitud, Plaza, TipoPlaza, HistorialOcupacion, RegistroClickPlaza
from app import db
from datetime import datetime, date
from sqlalchemy import extract, func, case, text
import json  # Importación necesaria para manejar datos JSON
from statsmodels.tsa.holtwinters import ExponentialSmoothing



routes = Blueprint('routes', __name__)


# Página principal: landing.html
@routes.route('/', methods=['GET'])
def home():
    return render_template('landing.html')

# Página de mapa de plazas
@routes.route('/mapa', methods=['GET', 'POST'])
def mapa():
    layout = {
        "superior": Plaza.query.filter(Plaza.id.between(1, 10)).all(),
        "bloque_izq": Plaza.query.filter(Plaza.id.between(11, 22)).all(),
        "bloque_der": Plaza.query.filter(Plaza.id.between(23, 44)).all(),
        "inferior": Plaza.query.filter(Plaza.id.between(45, 77)).all(),
    }

    if request.method == 'POST':
        space_id = int(request.form['space_id'])
        plaza = Plaza.query.get(space_id)
        if plaza:
            from app.models import HistorialOcupacion
            from datetime import datetime
            if not plaza.estado:  # Si estaba libre y pasa a ocupada
                plaza.estado = 1
                historial = HistorialOcupacion(
                    tipo_plaza_id=plaza.tipo_plaza_id,
                    plaza_id=plaza.id,
                    fecha=datetime.utcnow().date(),
                    hora_inicio=datetime.utcnow(),
                    hora_fin=None
                )
                db.session.add(historial)
            else:  # Si estaba ocupada y pasa a libre
                plaza.estado = 0
                ultimo = HistorialOcupacion.query.filter_by(
                    plaza_id=plaza.id, hora_fin=None
                ).order_by(HistorialOcupacion.hora_inicio.desc()).first()
                if ultimo:
                    ultimo.hora_fin = datetime.utcnow()
            db.session.commit()
        # Registrar el click
        registro = RegistroClickPlaza(plaza_id=space_id)
        db.session.add(registro)
        db.session.commit()
        return redirect(url_for('routes.mapa'))

    number_mapping = {
        1: 'B67', 2: 'B66', 3: 'B65', 4: 'B64', 5: 'B63', 6: 'B62', 7: 'B61', 8: 'B60', 9: 'B59', 10: 'B58',
        11: 'B41', 12: 'B42', 13: 'B43', 14: 'B44', 15: 'B45', 16: 'B46', 17: 'A39', 18: 'A38', 19: 'A37', 20: 'A36',
        21: 'A35', 22: 'A34', 23: 'B47', 24: 'B48', 25: 'B49', 26: 'B50', 27: 'B51', 28: 'B52', 29: 'B53', 30: 'B54',
        31: 'B55', 32: 'B56', 33: 'B57', 34: 'A33', 35: 'A32', 36: 'A31', 37: 'A30', 38: 'A29', 39: 'A28', 40: 'A27',
        41: 'A26', 42: 'A25', 43: 'A24', 44: 'A23', 45: 'M5', 46: 'M4', 47: 'M3', 48: 'M2', 49: 'M1', 50: 'A1',
        51: 'A2', 52: 'A3', 53: 'A4', 54: 'A5', 55: 'A6', 56: 'A7', 57: 'A8', 58: 'A9', 59: 'A10', 60: 'A11',
        61: 'A12', 62: 'A13', 63: 'A14', 64: 'A15', 65: 'A16', 66: 'A17', 67: 'A18', 68: 'A19', 69: 'A20', 70: 'A21',
        71: 'A22', 72: 'M11', 73: 'M10', 74: 'M9', 75: 'M8', 76: 'M7', 77: 'M6'
    }

    return render_template('index.html', layout=layout, number_mapping=number_mapping)

# --- Cambiar estado plaza vía AJAX ---
@routes.route('/toggle_estado/<int:plaza_id>', methods=['POST'])
def toggle_estado(plaza_id):
    from app.models import Plaza  # Importación dentro de la función
    plaza = Plaza.query.get_or_404(plaza_id)
    plaza.estado = not plaza.estado
    plaza.ultima_ocupacion = datetime.utcnow() if plaza.estado else None

    # Registrar en historial
    historial = HistorialOcupacion(
        plaza_id=plaza.id,
        tipo_plaza_id=plaza.tipo_plaza_id,
        fecha=datetime.utcnow().date(),
        hora_inicio=datetime.utcnow(),
        hora_fin=None if plaza.estado else datetime.utcnow()
    )
    db.session.add(historial)
    db.session.commit()

    return jsonify({'success': True, 'nuevo_estado': plaza.estado})


# --- Registrar click plaza (sin retorno de contenido) ---
@routes.route('/registrar_click/<int:plaza_id>', methods=['POST'])
def registrar_click(plaza_id):
    registro = RegistroClickPlaza(plaza_id=plaza_id)
    db.session.add(registro)
    db.session.commit()
    return '', 204

@routes.route('/conteo_multiple', methods=['GET'])
def conteo_multiple():
    tipo_plaza_filtro = request.args.get('tipo_plaza', None)
    fecha_filtro = request.args.get('fecha', None)

    # Datos de ejemplo con las plazas solicitadas
    datos_plazas = {
        "Motocicletas autorizadas": {"total": 20, "ocupadas": 10, "disponibles": 10},
        "Movilidad reducida": {"total": 15, "ocupadas": 8, "disponibles": 7},
        "Mujer embarazada": {"total": 10, "ocupadas": 5, "disponibles": 5},
        "Plaza asignada matrícula": {"total": 25, "ocupadas": 20, "disponibles": 5},
        "Plaza MOVILIDAD otros centros": {"total": 30, "ocupadas": 15, "disponibles": 15},
        "Plaza MOVILIDAD personal Of. Prov.": {"total": 40, "ocupadas": 30, "disponibles": 10},
        "Plaza VOLUNTARIADO": {"total": 50, "ocupadas": 30, "disponibles": 20},
        "Vehículos compartidos": {"total": 35, "ocupadas": 25, "disponibles": 10},
        "Vehículos de Cruz Roja": {"total": 10, "ocupadas": 7, "disponibles": 3},
    }

    datos_graficos = {
        "Motocicletas autorizadas": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [10, 12], "solicitudes": [5, 6]},
        "Movilidad reducida": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [8, 9], "solicitudes": [3, 4]},
        "Mujer embarazada": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [5, 6], "solicitudes": [2, 3]},
        "Plaza asignada matrícula": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [20, 22], "solicitudes": [8, 10]},
        "Plaza MOVILIDAD otros centros": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [15, 18], "solicitudes": [6, 7]},
        "Plaza MOVILIDAD personal Of. Prov.": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [30, 32], "solicitudes": [10, 12]},
        "Plaza VOLUNTARIADO": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [30, 35], "solicitudes": [10, 15]},
        "Vehículos compartidos": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [25, 28], "solicitudes": [8, 9]},
        "Vehículos de Cruz Roja": {"fechas": ["2025-06", "2025-07"], "ocupaciones": [7, 8], "solicitudes": [2, 3]},
    }

    # Aplicar filtro a los datos de la tabla
    if tipo_plaza_filtro:
        datos_plazas = {tipo: datos for tipo, datos in datos_plazas.items() if tipo == tipo_plaza_filtro}
        datos_graficos = {tipo: datos for tipo, datos in datos_graficos.items() if tipo == tipo_plaza_filtro}

    # Calcular solicitudes y ratio de ocupación
    datos_disponibilidad = {
        tipo: {
            "solicitadas": sum(datos["solicitudes"]),
            "ratio_ocupacion": round((datos_plazas[tipo]["ocupadas"] / datos_plazas[tipo]["total"]) * 100, 2)
            if datos_plazas[tipo]["total"] > 0 else 0
        }
        for tipo, datos in datos_graficos.items()
    }

    # Calcular totales
    total_conjunto = {
        "total": sum(datos["total"] for datos in datos_plazas.values()),
        "ocupadas": sum(datos["ocupadas"] for datos in datos_plazas.values()),
        "disponibles": sum(datos["disponibles"] for datos in datos_plazas.values()),
    }
    total_solicitadas = sum(
        datos["solicitadas"] for datos in datos_disponibilidad.values()
    )
    total_ratio_ocupacion = (
        (total_conjunto["ocupadas"] / total_conjunto["total"]) * 100
        if total_conjunto["total"] > 0
        else 0
    )

    # Calcular alertas de alta demanda
    alertas = []
    for tipo, datos in datos_graficos.items():
        solicitudes = sum(datos["solicitudes"])
        disponibles = datos_plazas.get(tipo, {}).get("disponibles", 0)
        if solicitudes > disponibles:
            alertas.append(
                f"Alta demanda para {tipo}: {solicitudes} solicitudes y solo {disponibles} disponibles."
            )

    return render_template(
        'conteo_multiple.html',
        datos_plazas=datos_plazas,
        datos_disponibilidad=datos_disponibilidad,
        datos_graficos_json=json.dumps(datos_graficos),
        total_conjunto=total_conjunto,
        total_solicitadas=total_solicitadas,
        total_ratio_ocupacion=round(total_ratio_ocupacion, 2),
        alertas=alertas,
        datos_plazas_todos=json.dumps({
            "Motocicletas autorizadas": {"total": 20, "ocupadas": 10, "disponibles": 10},
            "Movilidad reducida": {"total": 15, "ocupadas": 8, "disponibles": 7},
            "Mujer embarazada": {"total": 10, "ocupadas": 5, "disponibles": 5},
            "Plaza asignada matrícula": {"total": 25, "ocupadas": 20, "disponibles": 5},
            "Plaza MOVILIDAD otros centros": {"total": 30, "ocupadas": 15, "disponibles": 15},
            "Plaza MOVILIDAD personal Of. Prov.": {"total": 40, "ocupadas": 30, "disponibles": 10},
            "Plaza VOLUNTARIADO": {"total": 50, "ocupadas": 30, "disponibles": 20},
            "Vehículos compartidos": {"total": 35, "ocupadas": 25, "disponibles": 10},
            "Vehículos de Cruz Roja": {"total": 10, "ocupadas": 7, "disponibles": 3},
        })  # <-- Pasa aquí todos los datos, no los filtrados
    )



# --- Solicitar plaza (simplificado, implementar según necesidad) ---
@routes.route('/solicitar', methods=['POST'])
def solicitar():
    tipo_plaza_nombre = request.form.get('tipo_plaza')
    # Aquí implementar lógica para crear Solicitud y asignar plaza
    # Ejemplo simplificado:
    tipo_plaza = TipoPlaza.query.filter_by(descripcion=tipo_plaza_nombre).first()
    if not tipo_plaza:
        flash("Tipo de plaza no válido.", "danger")
        return redirect(url_for('routes.mapa'))

    solicitud = Solicitud(
        tipo_plaza_id=tipo_plaza.id,
        fecha_solicitud=datetime.utcnow(),
        estado='pendiente'
        # Otros campos que necesites
    )
    db.session.add(solicitud)
    db.session.commit()

    # Lógica para asignar plaza libre
    plaza_libre = Plaza.query.filter_by(tipo_plaza_id=tipo_plaza.id, estado=False).first()
    if plaza_libre:
        plaza_libre.estado = True
        db.session.commit()
        flash(f"Plaza asignada: {plaza_libre.id}", "success")
    else:
        flash("No hay plazas libres para este tipo.", "warning")

    return redirect(url_for('routes.mapa'))


# --- Reservar plaza voluntariado ---
@routes.route('/parking_access_volunteer', methods=['GET', 'POST'])
def parking_access_volunteer():
    if request.method == 'POST':
        tipo_plaza_id = int(request.form['tipo_plaza_id'])
        plaza_libre = Plaza.query.filter_by(tipo_plaza_id=tipo_plaza_id, estado=False).first()
        if plaza_libre:
            plaza_libre.estado = True
            db.session.commit()
            flash(f'¡Plaza {plaza_libre.tipo} reservada correctamente!', 'success')
        else:
            flash('No quedan plazas disponibles de ese tipo.', 'danger')
        return redirect(url_for('routes.parking_access_volunteer'))

    return render_template('parking_access_volunteer.html')

@routes.route('/toggle/<int:id>', methods=['POST'])
def toggle_plaza(id):
    from app import db
    from app.models import Plaza
    plaza = db.session.get(Plaza, id)
    if plaza:
        plaza.estado = 0 if plaza.estado else 1
        db.session.commit()
    return redirect(url_for('routes.mapa'))

@routes.route('/solicitudes_totales')
def solicitudes_totales():
    solicitudes_rows = db.session.execute(text("""
        SELECT tipo_plaza_id, COUNT(*) AS total_solicitudes
        FROM solicitudes
        GROUP BY tipo_plaza_id;
    """))
    resultados = [{"tipo_plaza_id": row[0], "total_solicitudes": row[1]} for row in solicitudes_rows]
    return jsonify(resultados)

@routes.route('/insertar_solicitud', methods=['POST'])
def insertar_solicitud():
    db.session.execute(text("""
        INSERT INTO solicitudes (solicitante_id, correo, ambito_id, frecuencia_id, tipo_plaza_id, mifare, plaza_id)
        VALUES (:solicitante_id, :correo, :ambito_id, :frecuencia_id, :tipo_plaza_id, :mifare, :plaza_id)
    """), {
        "solicitante_id": 1,
        "correo": "test@example.com",
        "ambito_id": 1,
        "frecuencia_id": 1,
        "tipo_plaza_id": 1,
        "mifare": "si",
        "plaza_id": None
    })
    db.session.commit()
    return jsonify({"success": True, "message": "Solicitud insertada correctamente"})

def predecir_ocupacion(datos_historicos):
    modelo = ExponentialSmoothing(datos_historicos, trend="add", seasonal="add", seasonal_periods=7)
    ajuste = modelo.fit()
    predicciones = ajuste.forecast(7)  # Predicción para los próximos 7 días
    return predicciones
