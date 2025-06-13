# En la carpeta data se encontrarian dos excels de nombres:
-  Plazas Movilidad y Voluntariado.xlsx: 
-  Vehículos compartidos.xlsx

```
├── data/
│   ├── excel_utils.py                           # Utilidades para cargar datos desde Excel.
│   ├── Plazas Movilidad y Voluntariado.xlsx     # Datos de plazas de movilidad y voluntariado.
│   └── Vehículos compartidos.xlsx               # Datos de vehículos compartidos.
```

## Ejemplo de como se veria Plazas Movilidad y Voluntariado.xlsx:
| Email              | Tipo de vehículo | Matrícula del vehículo | dias semana previsto | Fecha      | Fechafin | franja horaria prevista | tarjeta mifare | Ámbito            | Área | Departamento área Secretaría | Departamento área Coordinación | Oficina Autonómica | Asamblea Local | Necesidad                  | frecuencia mov prov | frecuencia mov cen | frecuencia vol | Estado    | Tipo Plaza                                                | Tipo de elemento | Ruta de acceso |
|--------------------|------------------|-------------------------|----------------------|------------|----------|--------------------------|----------------|-------------------|------|-------------------------------|-------------------------------|---------------------|----------------|----------------------------|---------------------|---------------------|----------------|-----------|------------------------------------------------------------|------------------|----------------|
| 03000-RRHH Leña    | Turismo          | 6666FBT                |                      | 6/17/2025  |          | De 7:30 a 19:30 h        | Sí             | Oficina Autonómica |      |                               | COA y personal ubicado en sede Alicante |                     |                | Menos de 1 vez/mes          |                     |                     |                | Rechazado | Movilidad personal Coordinación, Secretaría y AL Alicante | Elemento         |                |

## Ejemplo de como se veria Vehículos compartidos.xlsx:

| naps     | matrícula | Fecha Inicio | Fecha Fin  | acom1       | acom2       | acom3       | Estado    | Tipo de elemento | Ruta de acceso     |
|----------|-----------|--------------|------------|-------------|-------------|-------------|-----------|------------------|---------------------|
| 12345    | 1234ABC   | 2025-06-20   | 2025-06-21 | Juan Pérez  | Ana López   | -           | Aprobado  | Elemento         | Entrada principal   |