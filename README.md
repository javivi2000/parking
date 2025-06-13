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
│   ├── static/
│   |   ├── landing.css                          # Estilos para la página de inicio.
│   |   ├── parking_forms.css                    # Estilos para formularios.
│   |   ├── styles.css                           # Estilos del mapa de plazas.
│   |   └── js/
│   |       ├── index.js                         # Lógica JS del mapa interactivo de plazas.
│   |       └── conteo_multiple.js               # Lógica JS para gráficos y estadísticas.
│   |
│   └── templates/
│       ├── conteo_multiple.html                 # Panel de estadísticas con resumen y gráfico de ocupación.
│       ├── index.html                           # Mapa interactivo de plazas.
│       └──landing.html                          # Página de aterrizaje.
|
├── data/
│   ├── excel_utils.py                           # Utilidades para cargar datos desde Excel.
│   ├── Plazas Movilidad y Voluntariado.xlsx     # Datos de plazas de movilidad y voluntariado.
│   └── Vehículos compartidos.xlsx               # Datos de vehículos compartidos.
├── requirements.txt                             # Dependencias del proyecto.
├── README.md                                    # Documentación del proyecto.
└── run.py                                       # Punto de entrada de la aplicación.
```

## Descripción de Archivos y Carpetas

### Carpeta `app/`
Contiene el núcleo de la aplicación Flask.

- **`__init__.py`**  
  Inicializa la aplicación Flask, configura la base de datos (SQLAlchemy), y registra los Blueprints (módulos de rutas).  
  Si necesitas agregar nuevas rutas o módulos, aquí es donde se registran.

- **`config.py`**  
  Define la configuración global de la app, como la conexión a la base de datos, claves secretas, y otros parámetros de entorno.

- **`models.py`**  
  Define todos los modelos de la base de datos usando SQLAlchemy. Aquí se encuentran las clases que representan las tablas (usuarios, plazas, solicitudes, vehículos, etc).

- **`routes.py`**  
  Contiene las rutas principales de la aplicación, especialmente las relacionadas con el mapa de plazas y su gestión (libre/ocupado).


#### Carpeta `static/`
Archivos estáticos (CSS, JS, imágenes).

- **`landing.css`**  
  Estilos para la página de inicio.

- **`parking_forms.css`**  
  Estilos para los formularios de registro.

- **`styles.css`**  
  Estilos generales para el mapa de plazas y la interfaz principal.

- **`js/index.js`**  
  Lógica JavaScript para el mapa interactivo de plazas: manejo de clicks, matrículas, almacenamiento local, etc.

- **`js/conteo_multiple.js`**  
  Lógica JavaScript para la página de estadísticas y gráficos.

#### Carpeta `templates/`
Plantillas HTML renderizadas por Flask.

- **`index.html`**  
  Página principal con el mapa interactivo de plazas.

- **`landing.html`**  
  Página de bienvenida o inicio.

- **`parking_access_shared_vehicle.html`**  
  Formulario para registrar vehículos compartidos.

- **`parking_access_volunteer.html`**  
  Formulario para registrar voluntarios.

- **`conteo_multiple.html`**  
  Página de estadísticas y gráficos de ocupación.

---

### Carpeta `data/`
Archivos y utilidades para cargar y manejar datos externos.

- **`excel_utils.py`**  
  Funciones para importar y procesar datos desde archivos Excel.

- **`Plazas Movilidad y Voluntariado.xlsx`**  
  Archivo Excel con datos de plazas para movilidad y voluntariado.

- **`Vehículos compartidos.xlsx`**  
  Archivo Excel con datos de vehículos compartidos.

---

### Otros Archivos

- **`requirements.txt`**  
  Lista de dependencias de Python necesarias para el proyecto.

- **`README.md`**  
  Documentación principal: descripción general, instalación, uso y modelo de datos.

- **`run.py`**  
  Script principal para arrancar la aplicación Flask.

---

## Notas extra

- **Base de datos:**  
  El proyecto usa MySQL y SQLAlchemy. Los modelos están en `models.py` y la configuración en `config.py`.

- **Frontend:**  
  El mapa de plazas es interactivo gracias a JavaScript (`index.js`) y usa Bootstrap 5 para estilos.

- **Estadísticas:**  
  La página `/conteo_multiple` muestra gráficos y tablas dinámicas usando JS y datos de la base de datos.

- **Persistencia local:**  
  Algunas funciones (como matrículas temporales) usan LocalStorage del navegador.

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
- Flask-WTF  
- WTForms  
- Jinja2  
- Werkzeug  
- pandas  
- Bootstrap 5 (CDN, solo frontend)  
- Navegador moderno con soporte para LocalStorage y JavaScript

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


- **Gráficos y Estadísticas**: [http://127.0.0.1:5000/conteo_multiple](http://127.0.0.1:5000/conteo_multiple)  
  Visualiza estadísticas de ocupación y solicitudes en diferentes periodos.


## Características Técnicas Adicionales

- Estructura modular usando Blueprints de Flask.
- ORM completo con SQLAlchemy para una gestión robusta de la base de datos.
- Diseño responsivo con HTML/CSS personalizado.
- Actualización dinámica del estado de plazas mediante formularios y AJAX.


## Modelo de la Base de Datos (parking)

El modelo de datos se ha simplificado para centrarse únicamente en la gestión de plazas, su tipo y el registro de ocupaciones y clicks. Las tablas principales son:

```text
+-------------------+         +-------------------+
|    tipo_plaza     |         |      plaza        |
+-------------------+         +-------------------+
| id (PK)           |◄────────| tipo_plaza_id (FK)|
| descripcion       |         | id (PK)           |
+-------------------+         | estado            |
                              | tipo              |
                              | ultima_ocupacion  |
                              +-------------------+
                                       ▲
                                       │
                                       │
+------------------------+     +--------------------------+
| historial_ocupacion    |     | registro_click_plaza     |
+------------------------+     +--------------------------+
| id (PK)                |     | id (PK)                  |
| tipo_plaza_id (FK)     |     | plaza_id (FK)            |
| plaza_id (FK)          |     | timestamp                |
| fecha                  |     +--------------------------+
| hora_inicio            |
| hora_fin               |
+------------------------+
```

**Descripción de tablas:**

- **tipo_plaza**: Tipos de plaza (voluntariado, movilidad, etc).
- **plaza**: Plazas de estacionamiento, su estado y tipo.
- **historial_ocupacion**: Registro de ocupaciones y liberaciones de cada plaza.
- **registro_click_plaza**: Registro de cada click/cambio de estado en una plaza.

**Relaciones:**  
- Cada plaza puede tener un tipo (`tipo_plaza_id`).
- Cada registro de ocupación y click está vinculado a una plaza y, en el caso de ocupación, también a un tipo de plaza.

---


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


## Pendientes y errores identificados

- **Estadísticas (`conteo_multiple.html` / `conteo_multiple.js`)**  
  Las tablas *Plazas solicitadas* y *Solicitudes* no muestran correctamente los totales de solicitudes con estado **"Aprobado"** y **"Tarjeta actualizada"**. Falta integrar y filtrar adecuadamente los datos desde los Excel de SharePoint.

- **Mapa de plazas (`index.html` / `index.js`)**  
  Las plazas de motocicleta **M1 (ID 49)** y **M2 (ID 48)** no actualizan correctamente su estado al ocupar/desocupar ni asignan la matrícula de forma persistente. Es necesario revisar la lógica JS asociada a estas IDs.
