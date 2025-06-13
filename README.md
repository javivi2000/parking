# Aplicación de Gestión de Estacionamiento

Una aplicación web construida con Flask para gestionar espacios de estacionamiento y el acceso tanto para vehículos compartidos como para la movilidad de voluntarios. Los usuarios pueden solicitar plazas, visualizar su disponibilidad y registrar datos relevantes en formularios específicos.

## Estructura del Proyecto

```
parking-management-app
├── app/
│   ├── __init__.py                              # Inicializa la app Flask y registra componentes.
│   ├── config.py                                # Configuración de la aplicación y base de datos.
│   ├── models.py                                # Modelos de datos con SQLAlchemy.
│   ├── routes.py                                # Rutas para visualizar y gestionar plazas.
│   ├── views.py                                 # Rutas para formularios de vehículos compartidos y voluntarios.
│   └── static/
│   |   └── landing.css                          # Estilos para la página principal.
│   |   └── parking_shared_vehicle.css           # Estilos para el formulario de vehículo compartido.
│   |   └── parking_volunteer.css                # Estilos para el formulario de voluntarios.
│   |   └── styles.css                           # Estilos para del mapa de plazas.
│   │   ├── landing.css                          # Estilos para la página de inicio.
│   │   ├── parking_forms.css                    # Estilos para formularios.
│   │   └── styles.css                           # Estilos del mapa de plazas.
│   └── templates/
│       ├── conteo_multiple.html                 # Panel de estadísticas con resumen y gráfico de ocupación.
│       ├── index.html                           # Mapa interactivo de plazas.
│       ├── landing.html                         # Página de aterrizaje.
│       ├── parking_access_shared_vehicle.html   # Formulario para vehículos compartidos.
│       └── parking_access_volunteer.html        # Formulario para voluntarios.
├── requirements.txt                             # Dependencias del proyecto.
├── README.md                                    # Documentación del proyecto.
└── run.py                                       # Punto de entrada de la aplicación.
```
## Descripción de Archivos Clave

- **`__init__.py`**: Inicializa la aplicación Flask, configura SQLAlchemy y registra Blueprints. Usa `pymysql` para conectar con MySQL.
- **`config.py`**: Define la configuración principal de la app, incluyendo `SECRET_KEY` y la URI de la base de datos.
- **`models.py`**: Contiene todos los modelos de base de datos: solicitantes, vehículos, solicitudes, plazas, acompañantes, etc. Usa relaciones y claves foráneas para mantener integridad.
- **`routes.py`**: Define las rutas principales para visualizar y cambiar el estado de plazas (libre/ocupado). Incluye funciones para representar visualmente el mapa y actualizarlo en base a la BD.
- **`views.py`**: Agrupa rutas para manejar formularios de vehículos compartidos y voluntariado. Valida, procesa y guarda datos ingresados por los usuarios.

## Funcionalidades

- Visualización y gestión de 77 plazas de estacionamiento.
- Interfaz para cambiar el estado de ocupación de cada plaza con un solo clic.
- Formularios dinámicos para registrar solicitudes con datos completos.
- Persistencia de datos mediante base de datos MySQL y SQLAlchemy.
- **Estadísticas y gráficos interactivos**: Los usuarios pueden filtrar datos por tipo de plaza y mes en la ruta `/conteo_multiple`. Los gráficos y tablas se actualizan dinámicamente según los filtros aplicados.

## Requisitos

- Python 3.x  
- Flask  
- MySQL  
- pymysql  
- SQLAlchemy  

## Instrucciones de Instalación

1. Clona el repositorio:
   ```bash
   git clone <repository-url>
   cd parking-management-app
   ```
2. **Configura la base de datos**: Asegúrate de tener un servidor MySQL corriendo y crea una base de datos llamada `parking`.
3. **Actualiza la configuración**: Modifica el archivo `app/config.py` con tus credenciales de MySQL.
4. **Ejecuta la aplicación**:
   ```bash
   python run.py
   ```

Abre tu navegador en `http://127.0.0.1:5000`

## Uso

- **Mapa de Plazas**: [http://127.0.0.1:5000/mapa](http://127.0.0.1:5000/mapa)  
  Haz clic en una plaza para cambiar su estado (libre/ocupado).

- **Formulario Vehículo Compartido**: [http://127.0.0.1:5000/parking_access_shared_vehicle](http://127.0.0.1:5000/parking_access_shared_vehicle)  
  Completa los datos requeridos y guarda el registro.

- **Formulario Voluntariado**: [http://127.0.0.1:5000/parking_access_volunteer](http://127.0.0.1:5000/parking_access_volunteer)  
  Registra voluntarios y sus solicitudes con validaciones integradas.

- **Gráficos y Estadísticas**: [http://127.0.0.1:5000/conteo_multiple](http://127.0.0.1:5000/conteo_multiple)  
  Visualiza estadísticas de ocupación y solicitudes en diferentes periodos.


## Características Técnicas Adicionales

- Estructura modular usando Blueprints de Flask.
- ORM completo con SQLAlchemy para una gestión robusta de la base de datos.
- Diseño responsivo con HTML/CSS personalizado.
- Actualización dinámica del estado de plazas mediante formularios y AJAX.


## Modelo de la Base de Datos (parking)
```text
                 +----------------+         +----------------+
                 |    ambito      |         |   frecuencia   |
                 +----------------+         +----------------+
                 | id (PK)        |         | id (PK)        |
                 | descripcion    |         | descripcion    |
                 +----------------+         +----------------+

                 +----------------+         +----------------+
                 |  tipo_plaza    |         | franja_horaria |
                 +----------------+         +----------------+
                 | id (PK)        |         | id (PK)        |
                 | descripcion    |         | descripcion    |
                 +----------------+         +----------------+

                           ▲                        ▲
                           |                        |
                           |                        |
                           |                        |
                 +--------------------------+       |
                 |      solicitudes         |       |
                 +--------------------------+       |
                 | id (PK)                  |       |
                 | correo                   |       |
                 | ambito_id (FK) --------------+   |
                 | frecuencia_id (FK) ------------+ |
                 | tipo_plaza_id (FK) --------------+
                 | mifare (si/no)           |
                 | fecha_solicitud          |
                 +--------------------------+
                           ▲
                           |
        +------------------+------------------+
        |                                     |
  +-----------------------+        +--------------------------+
  | solicitud_dias_franjas|        |       vehiculos          |
  +-----------------------+        +--------------------------+
  | id (PK)               |        | id (PK)                  |
  | solicitud_id (FK) ----+        | solicitante_id (FK)      |
  | dias_semana           |        | matricula                |
  | franja_horaria_id (FK)|        +--------------------------+
  +-----------------------+

  +-------------------------+      +---------------------------+
  |      periodos_uso       |      |       acompanantes        |
  +-------------------------+      +---------------------------+
  | id (PK)                 |      | id (PK)                   |
  | solicitante_id (FK)     |      | solicitante_id (FK)       |
  | periodo_inicio          |      | nombre                    |
  | periodo_fin             |      | numero                    |
  +-------------------------+      +---------------------------+

  +--------------------------+     +---------------------------+
  |    historial_ocupacion   |     |           plaza           |
  +--------------------------+     +---------------------------+
  | id (PK)                  |     | id (PK)                   |
  | tipo_plaza_id (FK)       |     | estado (0/1)              |
  | plaza_id                 |     | tipo                      |
  | fecha                    |     | ultima_ocupacion          |
  | hora_inicio              |     +---------------------------+
  | hora_fin                 |
  +--------------------------+

  +--------------------------+
  | registro_click_plaza     |
  +--------------------------+
  | id (PK)                  |
  | plaza_id                 |
  | timestamp                |
  +--------------------------+
```


## Plazas y su 	ID / Código

| Tipo de Plaza 🅿️                       | ID y Código                   |
|-----------------------------------------|-------------------------------|
| 🟧 Voluntariado                         | 1: B67, 2: B66, 3: B65, 4: B64, 5: B63, 6: B62, 7: B61, 8: B60, 9: B59, 10: B58 |
| 🟪 Movilidad personal                   | 11: B41, 12: B42, 13: B43, 14: B44, 15: B45, 24: B48, 25: B49, 26: B50, 27: B51, 28: B52, 29: B53, 30: B54, 31: B55, 32: B56, 33: B57 |
| ♿ Movilidad reducida                   | 16: B46, 50: A1               |
| ◽ Plaza asignada matrícula             | 17: A39, 18: A38, 19: A37, 20: A36, 21: A35, 44: A23, 51: A2, 52: A3, 53: A4, 54: A5, 55: A6, 56: A7, 48: M2, 49: M1 |
| 🤰 Mujer embarazada                     | 22: A34, 23: B47              |
| 🟩 Vehículos compartidos                | 34: A33, 35: A32, 36: A31, 37: A30 |
| 🟨 Movilidad otros centros              | 38: A29, 39: A28, 40: A27, 41: A26 |
| 🟥 Vehículos de Cruz Roja               | 42: A25, 43: A24, 57: A8, 58: A9, 59: A10, 60: A11, 61: A12, 62: A13, 63: A14, 64: A15, 65: A16, 66: A17, 67: A18, 68: A19, 69: A20, 70: A21, 71: A22 |
| 🟦 Motocicletas autorizadas             | 45: M5, 46: M4, 47: M3, 48: M2, 49: M1, 72: M11, 73: M10, 74: M9, 75: M8, 76: M7, 77: M6 |


## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.