# Propuesta para implementar la pantalla “Disponibilidad” con estado histórico de ocupación

## 1. Contexto general del proyecto actual

- **Backend:** Flask + SQLAlchemy (ORM)  
- **Base de datos:** MySQL  
- **Frontend:** HTML con Jinja2 para renderizado dinámico + CSS + JavaScript para interacción y actualización dinámica.  
- **Arquitectura:**  
  - `app/` contiene la app Flask, con subcarpetas `static/` (CSS, JS), `templates/` (HTML), y módulos Python que implementan rutas (`views_*.py`), modelos (`models.py`), y configuración (`config.py`).  
- **Modelo de datos:** Representado con clases SQLAlchemy en `models.py`, acceso a través de objetos ORM, con consultas SQL detrás.  
- **Flujo MVC:**  
  - Modelo: `models.py`  
  - Vista (Frontend): HTML+Jinja2 en `templates/`  
  - Controlador: Rutas y funciones en módulos `views_*.py` que reciben peticiones, interactúan con modelo y devuelven vistas.

---

## 2. Nueva funcionalidad: Pantalla “Disponibilidad”

### 2.1 ¿Qué mostrar?

- Número de plazas solicitadas por tipo de plaza (por ejemplo, tipo “EF”, “FF”, etc.)  
- Ratio (plazas solicitadas / plazas totales disponibles) por tipo  
- Datos históricos de ocupación:  
  - Registro de estados de ocupación en base a día y hora (p.ej. 2/jun/2025 11:30 – plaza 6 – estado ocupado/libre)  
  - Poder consultar última medida (estado más reciente) y medias (promedios de ocupación) a lo largo del tiempo  
- Visualización gráfica y tabular de esta información para facilitar la interpretación y planificación.

### 2.2 ¿Para qué?

- Monitorizar en tiempo real y a posteriori la ocupación del parking  
- Poder tomar decisiones basadas en datos históricos (picos de ocupación, horas valle, etc.)  
- Integrar esta información en la interfaz actual de ubicación y gestión de plazas

---

## 3. Estructura técnica y planificación

### 3.1 Modelo de datos (Backend / `models.py`)

- Añadir tabla nueva para registro de estados de ocupación histórica, con al menos:  
  - `id`  
  - `fecha_hora` (datetime)  
  - `id_plaza` (FK a plazas)  
  - `estado` (ocupado/libre/otros estados posibles)  
  - Opcional: usuario o evento que asignó ese estado  
- Adaptar tablas existentes para poder cruzar datos tipo plaza, solicitudes, y estados históricos.  
- Consultas para:  
  - Obtener plazas solicitadas agrupadas por tipo en un rango de fechas  
  - Calcular ratios con plazas totales por tipo (datos ya almacenados o estáticos)  
  - Extraer última medida y media de ocupación en un período

### 3.2 Controlador / lógica de negocio (en `views_*`)

- Crear nuevas rutas y funciones Flask para:  
  - Obtener datos de ocupación y solicitudes desde el modelo (base de datos) en formato JSON (API REST)  
  - Procesar datos y preparar estadísticas (últimas medidas, medias)  
  - Controlar la grabación de nuevos estados de ocupación (posiblemente vía llamada AJAX o cron jobs)  
- Estas rutas deben integrarse dentro de un blueprint existente o uno nuevo, para modularidad.

### 3.3 Frontend / presentación (en `templates/` y `static/`)

- Nueva plantilla HTML para pantalla “Disponibilidad”:  
  - Tablas con número de plazas solicitadas y ratios por tipo  
  - Gráficos dinámicos para visualización temporal (se puede usar librerías JS populares para gráficos, p.ej. Chart.js, D3.js, u otra sencilla)  
  - Integrar con el CSS existente para mantener coherencia visual  
  - Opcional: filtros de fechas, tipos de plaza, etc.  
- JavaScript para:  
  - Consultar vía AJAX la API backend que devuelve datos de ocupación y estadísticas  
  - Actualizar dinámicamente la vista sin recarga completa  
  - Controlar interacción del usuario para explorar datos históricos

---

## 4. Frameworks y herramientas

- **Backend:** Flask + SQLAlchemy (ORM) + MySQL  
- **Frontend:**  
  - Jinja2 para renderizado inicial  
  - JavaScript + AJAX para actualización dinámica  
  - Librería gráfica recomendada: **Chart.js** (ligera, fácil de integrar)  
- **Organización:**  
  - Código backend separado en blueprints para orden y escalabilidad  
  - Plantillas HTML y archivos estáticos organizados en `templates/` y `static/`

---

## 5. Resumen: flujo de datos y componentes

| Componente       | Función principal                          | Ubicación/Archivos                         |
|------------------|-------------------------------------------|--------------------------------------------|
| Modelo de datos   | Guardar estados históricos y datos plazas | `app/models.py`                            |
| Controlador Flask | API para obtener/guardar datos, lógica negocio | `app/views_disponibilidad.py` (nuevo o integrado) |
| Plantilla HTML    | Pantalla “Disponibilidad” con tabla y gráficos | `app/templates/disponibilidad.html`       |
| JS y CSS         | Interactividad y estilo                    | `app/static/js/disponibilidad.js`, `app/static/css/disponibilidad.css` |
| Base de datos     | Tablas nuevas para historial y estados    | MySQL, migraciones/modificaciones          |

---

## 6. Consideraciones importantes

- Es fundamental planificar bien la estructura del modelo para el historial, pensando en volumen de datos y consultas eficientes.  
- La separación clara entre modelo, controlador y vista permitirá que futuros cambios o ampliaciones sean más sencillos.  
- Priorizar la usabilidad en la pantalla disponibilidad, haciendo la información clara y fácil de interpretar.  
- Revisar permisos y seguridad en la API para evitar acceso indebido a datos sensibles.  
- Validar que la captura de estados de ocupación sea automática o semi-automática para evitar errores.

---

## 7. Próximos pasos para la implementación

- Definir el esquema exacto para la tabla de estados históricos (campos, índices, etc.)  
- Crear prototipo inicial de la pantalla Disponibilidad en HTML con datos mock  
- Desarrollar rutas y lógica para obtención y cálculo de métricas  
- Integrar visualizaciones gráficas  
- Pruebas funcionales y de rendimiento con datos reales  
- Revisión y documentación

# Resumen
La nueva pantalla “Disponibilidad” mostrará de forma clara cuántas plazas hay solicitadas por tipo y su ratio respecto al total disponible. Además, registraremos el estado de ocupación de cada plaza a lo largo del tiempo para poder mostrar no solo el estado actual, sino también estadísticas históricas como promedios o picos de ocupación.

Para esto, añadiremos una tabla en la base de datos que guarde ese historial, y ampliaremos el backend con rutas que entreguen esos datos en JSON. En el frontend, crearemos una plantilla con tablas y gráficos interactivos (usando librerías como Chart.js) para visualizar y explorar esta información.

Todo se integrará en la estructura actual de Flask, cuidando modularidad, rendimiento y seguridad.

Los siguientes pasos son definir el esquema de la base de datos, crear un prototipo visual con datos simulados, desarrollar la API para manejar esos datos y finalmente integrar y probar la nueva pantalla.

Con esta funcionalidad tendremos un control mucho más completo y visual de la ocupación del parking, en tiempo real y a lo largo del tiempo, mejorando la toma de decisiones y la gestión.