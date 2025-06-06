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
    # Obtener filtros desde la solicitud
    tipo_plaza_filtro = request.args.get('tipo_plaza', None)
    fecha_filtro = request.args.get('fecha', None)

    # Validar tipo_plaza
    if tipo_plaza_filtro and not TipoPlaza.query.filter_by(descripcion=tipo_plaza_filtro).first():
        flash("Tipo de plaza no válido.", "danger")
        return redirect(url_for('routes.conteo_multiple'))

    # Validar fecha
    try:
        if fecha_filtro:
            datetime.strptime(fecha_filtro, '%Y-%m')  # Asegura que el formato sea YYYY-MM
    except ValueError:
        flash("Fecha no válida.", "danger")
        return redirect(url_for('routes.conteo_multiple'))

    # Datos para la tabla de resumen
    datos_plazas = {}
    total_conjunto = {"total": 0, "ocupadas": 0, "disponibles": 0}
    query = """
        SELECT 
            tp.descripcion AS tipo_plaza,
            COUNT(p.id) AS total,
            SUM(CASE WHEN p.estado = 1 THEN 1 ELSE 0 END) AS ocupadas,
            SUM(CASE WHEN p.estado = 0 THEN 1 ELSE 0 END) AS disponibles
        FROM plaza p
        RIGHT JOIN tipo_plaza tp ON p.tipo_plaza_id = tp.id
    """
    where_clauses = []
    if tipo_plaza_filtro:
        where_clauses.append("tp.descripcion = :tipo_plaza")
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " GROUP BY tp.descripcion ORDER BY tp.descripcion"

    rows = db.session.execute(text(query), {"tipo_plaza": tipo_plaza_filtro})
    for row in rows:
        tipo = row[0]
        total = int(row[1])
        ocupadas = int(row[2])
        disponibles = int(row[3])
        datos_plazas[tipo] = {
            "total": total,
            "ocupadas": ocupadas,
            "disponibles": disponibles
        }
        total_conjunto["total"] += total
        total_conjunto["ocupadas"] += ocupadas
        total_conjunto["disponibles"] += disponibles

    # Datos para la tabla de disponibilidad
    datos_disponibilidad = {}
    total_solicitadas = 0
    solicitudes_query = """
        SELECT 
            tp.descripcion AS tipo_plaza,
            COUNT(s.id) AS solicitadas
        FROM tipo_plaza tp
        LEFT JOIN solicitudes s ON s.tipo_plaza_id = tp.id
    """
    if where_clauses:
        solicitudes_query += " WHERE " + " AND ".join(where_clauses)
    solicitudes_query += " GROUP BY tp.descripcion"

    solicitudes_rows = db.session.execute(text(solicitudes_query), {"tipo_plaza": tipo_plaza_filtro})
    for row in solicitudes_rows:
        tipo = row[0]
        solicitadas = int(row[1])
        disponibles = datos_plazas[tipo]["disponibles"] if tipo in datos_plazas else 0
        total = datos_plazas[tipo]["total"] if tipo in datos_plazas else 0
        ratio = round((solicitadas / total) * 100, 2) if total > 0 else 0
        datos_disponibilidad[tipo] = {
            "total_disponibles": disponibles,
            "solicitadas": solicitadas,
            "ratio_ocupacion": ratio
        }
        total_solicitadas += solicitadas

    # Calcular alertas
    alertas = []
    for tipo, datos in datos_disponibilidad.items():
        if datos["solicitadas"] > datos["total_disponibles"]:
            alertas.append(f"Alta demanda para {tipo}: {datos['solicitadas']} solicitudes y solo {datos['total_disponibles']} disponibles.")

    # Calcular el ratio de ocupación total
    total_ratio_ocupacion = round((total_conjunto["ocupadas"] / total_conjunto["total"]) * 100, 2) if total_conjunto["total"] > 0 else 0

    # Crear datos para los gráficos agrupados por mes
    datos_graficos = {}
    historial_query = """
        SELECT 
            tp.descripcion AS tipo_plaza,
            DATE_FORMAT(ho.fecha, '%Y-%m') AS mes,  -- Agrupa por mes y año
            COUNT(ho.id) AS ocupaciones
        FROM historial_ocupacion ho
        JOIN tipo_plaza tp ON ho.tipo_plaza_id = tp.id
    """
    if fecha_filtro:
        historial_query += " WHERE DATE_FORMAT(ho.fecha, '%Y-%m') = :fecha"
    historial_query += " GROUP BY tp.descripcion, DATE_FORMAT(ho.fecha, '%Y-%m') ORDER BY tp.descripcion, mes"

    historial_rows = db.session.execute(text(historial_query), {"fecha": fecha_filtro})
    for row in historial_rows:
        tipo = row[0]
        mes = row[1]  # Ahora es el mes en formato 'YYYY-MM'
        ocupaciones = int(row[2])
        if tipo not in datos_graficos:
            datos_graficos[tipo] = {"fechas": [], "ocupaciones": [], "solicitudes": []}
        datos_graficos[tipo]["fechas"].append(mes)
        datos_graficos[tipo]["ocupaciones"].append(ocupaciones)

    # Agregar datos de solicitudes agrupados por mes
    solicitudes_query = """
        SELECT 
            tp.descripcion AS tipo_plaza,
            DATE_FORMAT(s.fecha_solicitud, '%Y-%m') AS mes,  -- Agrupa por mes y año
            COUNT(s.id) AS solicitudes
        FROM solicitudes s
        JOIN tipo_plaza tp ON s.tipo_plaza_id = tp.id
    """
    if fecha_filtro:
        solicitudes_query += " WHERE DATE_FORMAT(s.fecha_solicitud, '%Y-%m') = :fecha"
    solicitudes_query += " GROUP BY tp.descripcion, DATE_FORMAT(s.fecha_solicitud, '%Y-%m') ORDER BY tp.descripcion, mes"

    solicitudes_rows = db.session.execute(text(solicitudes_query), {"fecha": fecha_filtro})
    for row in solicitudes_rows:
        tipo = row[0]
        mes = row[1]  # Ahora es el mes en formato 'YYYY-MM'
        solicitudes = int(row[2])
        if tipo not in datos_graficos:
            datos_graficos[tipo] = {"fechas": [], "ocupaciones": [], "solicitudes": []}
        if mes not in datos_graficos[tipo]["fechas"]:
            datos_graficos[tipo]["fechas"].append(mes)
            datos_graficos[tipo]["ocupaciones"].append(0)  # Asegura que ocupaciones tenga un valor
        datos_graficos[tipo]["solicitudes"].append(solicitudes)

    return render_template(
        'conteo_multiple.html',
        datos_plazas=datos_plazas,
        total_conjunto=total_conjunto,
        datos_graficos=datos_graficos,
        datos_graficos_json=json.dumps(datos_graficos),
        datos_disponibilidad=datos_disponibilidad,
        total_solicitadas=total_solicitadas,
        total_ratio_ocupacion=total_ratio_ocupacion,
        alertas=alertas
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
