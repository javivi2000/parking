import os
import pandas as pd
import math

def cargar_plazas():
    """
    Lee el archivo de plazas y devuelve una lista de diccionarios con los campos principales y todos los extras.
    """
    df = pd.read_excel('data/Plazas Movilidad y Voluntariado.xlsx')
    plazas = []
    for _, row in df.iterrows():
        plaza = {
            'id': row.get('ID', None),
            'tipo_plaza': row.get('Tipo Plaza', None),
            'estado': row.get('Ocupada', None),
            'ultima_ocupacion': row.get('Última ocupación', None)
        }
        # Añadir todos los campos extra del Excel, normalizados
        for col in df.columns:
            key = col.strip().lower().replace(" ", "_")
            if key not in plaza:
                plaza[key] = row[col]
        plazas.append(plaza)
    return plazas

def cargar_solicitudes():
    """
    Lee todos los archivos de solicitudes en la carpeta data/ y devuelve una lista de diccionarios
    con los campos principales y todos los extras.
    El campo 'estado' puede tener valores como: 'Pendiente', 'Rechazado', 'Tarjeta Actualizada', 'Aprobado y tarjeta actualizada', etc.
    """
    solicitudes = []
    data_folder = 'data'
    for fname in os.listdir(data_folder):
        if fname.endswith('.xlsx') and 'plaza' not in fname.lower():
            df = pd.read_excel(os.path.join(data_folder, fname))
            for _, row in df.iterrows():
                tipo_plaza = row.get('Tipo Plaza', None)
                if tipo_plaza is None:
                    tipo_plaza = row.get('Tipo de elemento', None)
                estado = row.get('Estado', None)
                if tipo_plaza is not None and isinstance(tipo_plaza, float) and math.isnan(tipo_plaza):
                    tipo_plaza = ''
                if estado is not None and isinstance(estado, float) and math.isnan(estado):
                    estado = ''
                solicitud = {
                    'tipo_plaza_id': tipo_plaza,
                    'estado': estado
                }
                solicitudes.append(solicitud)
    print("Solicitudes crudas:")
    for s in solicitudes:
        print(s)
    return solicitudes

def cargar_tipos_plaza():
    """
    Devuelve la lista de tipos de plaza únicos del archivo de plazas.
    """
    df = pd.read_excel('data/Plazas Movilidad y Voluntariado.xlsx')
    tipo_col = next((col for col in df.columns if col.strip().lower() in ['tipo plaza', 'tipo_plaza_id']), None)
    if tipo_col:
        return sorted(df[tipo_col].dropna().unique().tolist())
    return []

"""
Funciones para cargar datos desde archivos Excel en la carpeta 'data':

- cargar_plazas(): Lee el archivo de plazas y devuelve una lista con toda la información de cada plaza.
- cargar_solicitudes(): Lee todos los archivos de solicitudes (excepto plazas) y devuelve una lista con datos y estado de cada solicitud.
- cargar_tipos_plaza(): Extrae y devuelve la lista única de tipos de plaza desde el archivo de plazas.
"""
