from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import Plaza, TipoPlaza, HistorialOcupacion, RegistroClickPlaza
from app import db
from datetime import datetime, timedelta
from sqlalchemy import desc
from data.excel_utils import cargar_plazas, cargar_solicitudes
import unicodedata


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


# --- Registrar click plaza ---
@routes.route('/registrar_click/<int:plaza_id>', methods=['POST'])
def registrar_click(plaza_id):
    registro = RegistroClickPlaza(plaza_id=plaza_id)
    db.session.add(registro)
    db.session.commit()
    return '', 204

import unicodedata
from flask import render_template
from data.excel_utils import cargar_solicitudes

def normaliza(texto):
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto).strip().lower())
        if unicodedata.category(c) != 'Mn'
    )

@routes.route('/conteo_multiple', methods=['GET'])
def conteo_multiple():
    limites_plazas = {
        "Vehiculos compartidos": 4, 
        "Plaza asignada matrícula": 14,
        "Vehículo Cruz Roja plaza asignada matrícula": 17,
        "Voluntaríado": 10,
        "Mujer embarazada": 2,
        "Personal con movilidad reducida": 2,
        "Motocicletas y ciclomotores autorizados": 9,
        "Movilidad personal Coordinación, Secretaría y AL Alicante": 15,
        "Bicicletas y patinetes autorizados": 0,
        "Movilidad otros centros y visitas externos": 4,
    }

    tipos_plaza_fijos = [
        "Vehiculos compartidos",
        "Plaza asignada matrícula",
        "Vehículo Cruz Roja plaza asignada matrícula",
        "Voluntaríado",
        "Mujer embarazada",
        "Personal con movilidad reducida",
        "Motocicletas y ciclomotores autorizados",
        "Movilidad personal Coordinación, Secretaría y AL Alicante",
        "Bicicletas y patinetes autorizados",
        "Movilidad otros centros y visitas externos",
    ]

    MAPEO_TIPO_RESUMEN_A_BD = {
        "Vehiculos compartidos": "Vehículos compartidos",
        "Plaza asignada matrícula": "Plaza asignada matrícula",
        "Vehículo Cruz Roja plaza asignada matrícula": "Vehículos de Cruz Roja",
        "Voluntaríado": "Plaza VOLUNTARIADO",
        "Mujer embarazada": "Mujer embarazada",
        "Personal con movilidad reducida": "Movilidad reducida",
        "Motocicletas y ciclomotores autorizados": "Motocicletas autorizadas",
        "Movilidad personal Coordinación, Secretaría y AL Alicante": "Movilidad personal Coordinación, Secretaría y AL Alicante",
        "Bicicletas y patinetes autorizados": "Bicicletas y patinetes autorizados",
        "Movilidad otros centros y visitas externos": "Movilidad otros centros y visitas externos",
    }

    # Solo se consideran solicitudes con estado "Tarjeta Actualizada" o "Aprobado"
    estados_validos = [normaliza('aprobado'), normaliza('tarjeta actualizada')]
    solicitudes = cargar_solicitudes()
    solicitudes_filtradas = [
        s for s in solicitudes
        if normaliza(s.get('estado', '')) in estados_validos
    ]

    # Agrupa por tipo de plaza del Excel
    solicitudes_por_tipo = {}
    for resumen, nombre_excel in MAPEO_TIPO_RESUMEN_A_BD.items():
        nombre_excel_norm = normaliza(nombre_excel)
        solicitudes_por_tipo[resumen] = sum(
            1 for s in solicitudes_filtradas
            if normaliza(s.get('tipo_plaza_id', '')) == nombre_excel_norm
        )

    solicitadas_por_tipo = solicitudes_por_tipo.copy()
    total_solicitudes_por_tipo = solicitudes_por_tipo.copy()

    ocupadas_por_tipo = {}
    disponibles_por_tipo = {}
    porcentaje_ocupacion = {}

    for resumen, bd in MAPEO_TIPO_RESUMEN_A_BD.items():
        tipo = TipoPlaza.query.filter(TipoPlaza.descripcion == bd).first()
        if tipo:
            ocupadas = Plaza.query.filter_by(tipo_plaza_id=tipo.id, estado=True).count()
        else:
            ocupadas = 0
        total = limites_plazas[resumen]
        ocupadas_por_tipo[resumen] = ocupadas
        disponibles_por_tipo[resumen] = total - ocupadas

        # Plazas solicitadas: contar solicitudes aprobadas
        solicitadas_por_tipo[resumen] = solicitudes_por_tipo.get(resumen, 0)

        # Porcentaje de ocupación
        if total > 0:
            porcentaje = round((ocupadas / total) * 100, 1)
        else:
            porcentaje = 0
        porcentaje_ocupacion[resumen] = porcentaje

    total_plazas = sum(limites_plazas[tipo] for tipo in tipos_plaza_fijos)
    total_ocupadas = sum(ocupadas_por_tipo[tipo] for tipo in tipos_plaza_fijos)
    total_disponibles = sum(disponibles_por_tipo[tipo] for tipo in tipos_plaza_fijos)
    total_solicitadas = sum(solicitadas_por_tipo[tipo] for tipo in tipos_plaza_fijos)
    # % Ocupación global (sobre el total de plazas)
    if total_plazas > 0:
        total_porcentaje_ocupacion = round((total_ocupadas / total_plazas) * 100, 1)
    else:
        total_porcentaje_ocupacion = 0

    plazas_excel = cargar_plazas()  # Lista de dicts con clave 'tipo'
    total_plazas_excel = {}
    for tipo in tipos_plaza_fijos:
        total_plazas_excel[tipo] = sum(1 for p in plazas_excel if p['tipo_plaza'] == tipo)

    # --- Cálculo del porcentaje de demanda ---
    porcentaje_demanda = {}
    for tipo in tipos_plaza_fijos:
        total = total_plazas_excel.get(tipo, 0)
        solicitadas = solicitadas_por_tipo.get(tipo, 0)
        if total > 0:
            porcentaje_demanda[tipo] = round((solicitadas / total) * 100, 1)
        else:
            porcentaje_demanda[tipo] = 0

    ultima_ocupacion = {}
    media_ocupacion = {}

    for tipo in tipos_plaza_fijos:
        # Obtén los ids de plazas de este tipo
        plazas_ids = [p.id for p in Plaza.query.filter_by(tipo=tipo).all()]

        ultima = (
            HistorialOcupacion.query
            .filter(HistorialOcupacion.plaza_id.in_(plazas_ids))
            .order_by(desc(HistorialOcupacion.hora_inicio)) 
            .first()
        )
        if ultima:
            ultima_ocupacion[tipo] = {
                'fecha': ultima.hora_inicio.strftime('%d/%m/%Y %H:%M'),  
                'estado': 'ocupada' if ultima.hora_fin is None else 'libre'
            }
        else:
            ultima_ocupacion[tipo] = {'fecha': 'Sin datos', 'estado': '-'}

        # Media de ocupación (últimos 30 días)
        desde = datetime.now() - timedelta(days=30)
        registros = (
            HistorialOcupacion.query
            .filter(HistorialOcupacion.plaza_id.in_(plazas_ids))
            .filter(HistorialOcupacion.hora_inicio >= desde)  
            .all()
        )
        if registros:
            ocupadas = sum(1 for r in registros if r.hora_fin is None)
            media = round((ocupadas / len(registros)) * 100, 1)
            media_ocupacion[tipo] = media
        else:
            media_ocupacion[tipo] = 0

    total_solicitudes_por_tipo = {}
    for tipo in tipos_plaza_fijos:
        # Mostrar solicitudes aprobadas por tipo
        total_solicitudes_por_tipo[tipo] = solicitudes_por_tipo.get(tipo, 0)

    print("Valores únicos de estado normalizados:")
    print(set(normaliza(s.get('estado', '')) for s in solicitudes))

    print("Valores únicos de tipo_plaza_id en solicitudes:")
    print(set(normaliza(str(s.get('tipo_plaza_id', ''))) for s in solicitudes_filtradas))
    print("Valores normalizados del mapeo:")
    print([normaliza(MAPEO_TIPO_RESUMEN_A_BD[tipo]) for tipo in tipos_plaza_fijos])

    return render_template(
        'conteo_multiple.html',
        tipos_plaza=tipos_plaza_fijos,
        limites_plazas=limites_plazas,  
        solicitadas_por_tipo=solicitadas_por_tipo,
        total_solicitudes_por_tipo=total_solicitudes_por_tipo,
        ocupadas_por_tipo=ocupadas_por_tipo,
        disponibles_por_tipo=disponibles_por_tipo,
        porcentaje_ocupacion=porcentaje_ocupacion,
        total_plazas=total_plazas,
        total_ocupadas=total_ocupadas,
        total_disponibles=total_disponibles,
        total_solicitadas=total_solicitadas,
        total_porcentaje_ocupacion=total_porcentaje_ocupacion,
        porcentaje_demanda=porcentaje_demanda,
        total_plazas_excel=total_plazas_excel,
        ultima_ocupacion=ultima_ocupacion,
        media_ocupacion=media_ocupacion,
    )

# Mapeo de nombres resumen -> nombres en la BBDD
MAPEO_TIPO_RESUMEN_A_BD = {
    "Vehiculos compartidos": "Vehículos compartidos",
    "Plaza asignada matrícula": "Plaza asignada matrícula",
    "Vehículo Cruz Roja plaza asignada matrícula": "Vehículos de Cruz Roja",
    "Voluntaríado": "Plaza VOLUNTARIADO",
    "Mujer embarazada": "Mujer embarazada",
    "Personal con movilidad reducida": "Movilidad reducida",
    "Motocicletas y ciclomotores autorizados": "Motocicletas autorizadas",
    "Movilidad personal Coordinación, Secretaría y AL Alicante": "Movilidad personal Coordinación, Secretaría y AL Alicante",
    "Bicicletas y patinetes autorizados": "Bicicletas y patinetes autorizados",  
    "Movilidad otros centros y visitas externos": "Movilidad otros centros y visitas externos",
}


"""
Define las rutas principales de la app de gestión de aparcamiento:

- '/' y '/mapa': Renderiza el mapa interactivo de plazas y permite cambiar su estado.
- '/conteo_multiple': Muestra estadísticas de ocupación por tipo de plaza.
- '/cargar_datos_excel': Importa datos de plazas desde un archivo Excel.
- '/toggle_estado/<id>': Alterna el estado de una plaza y guarda el historial.

Utiliza los modelos Plaza, TipoPlaza, RegistroClickPlaza y HistorialOcupacion.
"""
