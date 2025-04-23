import os
import mysql.connector
from mysql.connector import Error

def create_connection(host, port, user, password, database):
    try:
        connection = mysql.connector.connect(
            host= host,
            port= port,
            user= user,
            password= password,
            database= database
        )

        if connection.is_connected():                
            return connection
        
    except Error as e:
        return None


def execute_query(connection, query, params=None):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


if __name__ == "__main__":
    with create_connection() as conn:
        if conn:
            print("Conexión establecida correctamente.")
        else:
            print("No se pudo establecer la conexión.")

    # consulta = "SELECT * FROM tabla_ejemplo WHERE columna = %s"
    # parametros = ("valor",)  # Tuple con parámetros para evitar inyecciones SQL
    # resultados = ejecutar_consulta(consulta, parametros)

    # if resultados:
    #     for fila in resultados:
    #         print(fila)
