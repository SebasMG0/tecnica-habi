# Prueba técnica Habi

## Tecnologías a utilizar
El desarrollo se llevará a cabo utilizando python. Dadas las condiciones de implementación se evita el uso de frameworks como flask o fastapi, por lo que se utilizará librerías de python para el manejo de variables de entorno, conectores para la base de datos y soporte para el desarrollo de consultas http:
- *dotenv*
- *mysql-connector-python*
- *http*
- *venv*

## Estructura de desarrollo
### Estructura de Carpetas
Se utilizará un entorno virtual administrado con la librería *venv* en una carpeta con el mismo nombre. En la carpeta *database* se encuentra el código necesario para la conexión con la base de datos y sus respectivas peticiones. Las clases destinadas a representar entidades se encuentran en el directorio *model* y funciones adicionales como de verificación estarán almacenadas en la carpeta utils.

La aplicación se inicia desde el archivo *main.py* que se encuentra en la raiz del proyecto y requiere la utilización de un archivo *.env* con la información necesaria para la conexión con la base de datos. Es decir, se requieren las variables:
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
├── model
├── utils
|── venv
└── main.py
```
