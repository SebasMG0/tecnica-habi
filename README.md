# Prueba Técnica Habi
Sebastián Murcia Gómez - s.murciag@uniandes.edu.co

## Tecnologías a utilizar
El desarrollo se llevará a cabo utilizando python. Dadas las condiciones de implementación se evita el uso de frameworks como flask o fastapi, por lo que se utilizará librerías de python para el manejo de variables de entorno, conectores para la base de datos y soporte para el desarrollo de consultas http. En particular, se utilizan las librerías:
- *dotenv*
- *mysql-connector-python*
- *http*
- *pytest*
- *venv*

## Desarrollo
### Estructura de Carpetas
Se utilizará un entorno virtual administrado con la librería *venv* en carpeta con el mismo nombre. En la carpeta *database* se encuentra el código necesario para la conexión con la base de datos y la ejecución de consultas sql. El controlador que actúa como intermediario entre la api y la base de datos se encuentra en la carpeta *controller*. Dicho controlador cuenta con funciones para construir la consulta sql requerida para la obtención de los inmuebles con la aplición de filtros opcionales y realiza la validación de dichos filtros. Además ejecuta la consulta sql y retorna el resultado de la misma en formato JSON. Por último, se añdió una carpeta *test* con el propósito de alojar las pruebas unitarias del código.

La aplicación se ejecuta desde el archivo *main.py* que se encuentra en la raiz del proyecto y requiere la utilización de un archivo *.env* con la información necesaria para la conexión con la base de datos. Es decir, se requieren las variables:

```
HOST: host_example
PORT: port_example
USER: user_example
PASS: password_example
SCHEMA: schema_example
```

De este modo, la estructura de carpetas propuesta para el cumplimiento de los requerimientos es:

```
├── api
├── database
├── controller
├── test
|── venv
└── main.py
```

El proceso de desarrollo inició con la creacioń del conector para la base de datos, osteriormente se definió el endpoint y el tipo la estructura de datos de la información recibida del frontend  para dar cumplimiento a los requisitos del primer requerimiento. Por último se realizó el controlador destinado a servir de puente entre la api y la base de datos para continuar con las pruebas unitarias de los principales componentes de la aplicación.

### Aspectos a Tomar en Cuenta

#### Filtros
Dado que se menciona que se pueden aplicar multiples filtros se realizaron las siguiente suposiciones:

- Cuando un usuario introduce 1 año particular como filtro, el sistema retorna solo los inmuebles que fueron construidos en ese año en particular que cumplan con el resto de filtros si es el caso.

- Cuando se introducen 2 años, el sistema retorna los inmuebles que fueron construidos en el rango de fechas entre los dos años.

- Si se introducen mas de 2 años, el sistema retorna los inmuebles construidos en esos años en particular.

- Es posible filtrar por más de una ciudad

- Es posible filtrar por más de un estado y no se permite estados diferentes a 3, 4 y 5; Pre_venta, en_venta y vendido respectivamente.

- La información de los inmuebles que se muestra corresponde a los valores *status*, *city*, *address*, *year*, *price* y *description*.

### Ejecución
Para ejecutar la aplicación se hace necesario cumplir con los siguientes requerimientos:

- Creación de un entorno virutal con *venv* y la instalación de las dependencias enumeradas en el archivo *requirements.txt*

- Creación de un archivo *.env* en la raiz del proyecto con las variables que se mencionaron en el apartado *Estructura de Carpetas*

- Ejecución del archivo *main.py*

### Pruebas Unitarias
Para ejecutar las pruebas unitarias y explorar su cobertura total se ejecuta el comando:

```bash
pytest --cov
```

### Información del Frontend
Se espera que el frontend envíe en formato .json los campos por los cuales se van a filtrar los resultados. Algunos ejemplos válidos se muestran a continuación:

```json
{
    "status": [3, 4],
    "year": [2010, 2024],
    "city": ["bogota", "medellin", "cali"]
}
```
```json
{
    "status": [3, 4]
}
```

```json
{
    "year": [2015]
}
```

También es posible no enviar ninguna información en el cuerpo de la petición.

## Requerimiento 2: *Me Gusta*

Para añadir soporte para implementar me gusta a los usuarios registrados se añade la tabla *like_history*, en la cual se guardan los campos que referencian los ids de las propiedades a las cuales los usuarios identificados con un id les dan like. De este modo es posible guardar el historial de likes de un usuario que se halla registrado sin degradar la normalización de la base de datos y utilizando la tabla *auth_user* que ya se encuentra creada. Además, el campo *update_date* ayuda a llevar una traza del comportamiento de un usuario con sus respectivos gustos por determinados inmuebles.

![Tecnica HABI REQ2](https://github.com/user-attachments/assets/5bc3d167-ee14-4f35-b77b-89d9a0308e43)


El código para la creación de la tabla *like_history* y las restricciones de llave foránea necesarias para extender el modelo se muestra a continuación:

```sql

CREATE TABLE like_history(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE like_history
ADD CONSTRAINT fk_property FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE;

```
