# Aplicación de Gestión de Estacionamiento

Este proyecto es una aplicación web para gestionar plazas de estacionamiento. Permite a los usuarios ocupar o liberar plazas a través de una sencilla interfaz web.

## Estructura del Proyecto

```
parking-management-app
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── templates
│       └── index.html
├── requirements.txt
└── README.md
```

## Funcionalidades

- Gestiona 38 plazas de estacionamiento.
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
   python app/main.py
   ```

4. Abre tu navegador y navega a `http://127.0.0.1:5000` para acceder a la aplicación.

## Uso

- Haz clic en una plaza para ocuparla.
- Haz clic en una plaza ocupada para liberarla.
- La interfaz se actualizará para reflejar el estado actual de cada plaza.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.