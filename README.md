# Aplicación de Gestión de Estacionamiento

Una aplicación web construida con Flask para gestionar espacios de estacionamiento y el acceso al estacionamiento tanto para vehículos compartidos como para la movilidad de voluntarios. La aplicación permite a los usuarios solicitar espacios de estacionamiento, gestionar su acceso y manejar la información de vehículos compartidos para una gestión eficiente de los recursos de estacionamiento.

## Estructura del Proyecto

```
parking-management-app
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── views_shared_vehicle.py
│   ├── views_volunteer.py
│   └── static/
│   |   └── parking_shared_vehicle.css
│   |   └── parking_volunteer.css
│   |   └── styles.css
│   └── templates/
│       └── index.html
│       └── parking_access_shared_vehicle.html
│       └── parking_access_volunteer.html
├── requirements.txt
├── README.md
└── run.py
```
## Descripción

El proyecto consta de dos formularios principales que permiten a los usuarios gestionar solicitudes de plaza de parking:

1. Formulario para vehículos compartidos: Permite a los solicitantes registrar un vehículo compartido para solicitar una plaza de parking.

2. Formulario para movilidad/voluntariado: Permite a los voluntarios o empleados gestionar el acceso al parking para propósitos de movilidad.

Los usuarios pueden visualizar la disponibilidad de 77 plazas de estacionamiento y marcar una plaza como ocupada o libre.

## Funcionalidades

- Gestiona 77 plazas de estacionamiento.
- Los usuarios pueden ocupar o liberar una plaza haciendo clic sobre ella.
- Actualizaciones en tiempo real de la disponibilidad de plazas.

## Requisitos

- Python 3.x
- Flask

## Instrucciones de Instalación

1. Clona el repositorio:
   ```
   git clone <repository-url>
   cd parking-management-app
   ```

2. Instala los paquetes requeridos:
   ```
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```
   python run.py
   ```

4. Abre tu navegador y navega a `http://127.0.0.1:5000` para acceder a la aplicación.

## Uso

- Gestionar plazas de parking: Haz clic en una plaza para ocuparla. Haz clic en una plaza ocupada para liberarla.

- Acceso al formulario de vehículos compartidos: Ve a http://127.0.0.1:5000/parking_access_shared_vehicle.

- Acceso al formulario de voluntariado/movilidad: Ve a http://127.0.0.1:5000/parking_access_volunteer.

- Gestión de solicitudes: Los usuarios pueden completar los formularios con sus datos, vehiculos, y periodos de uso. Los acompañantes también pueden ser registrados.

### Funcionalidades Adicionales
- Modelo de Plazas de Parking: Un total de 77 plazas, organizadas en bloques, con un estado que puede cambiar de libre a ocupada.

- Formulario de Solicitud: La información se guarda en una base de datos MySQL, gestionando las relaciones entre solicitantes, vehículos, acompañantes, y periodos de uso.

- Base de Datos: Se utiliza MySQL con SQLAlchemy, incluyendo la configuración y modelos correspondientes para las solicitudes y demás datos.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.