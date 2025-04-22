import os
from dotenv import load_dotenv
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
            with connection.cursor() as cursor:
                cursor.execute("show tables")
                for tabla in cursor.fetchall():
                    print(tabla)

                cursor.execute("select * from status_history")
                print(cursor.fetchall()[0])

                cursor.execute("SELECT * from status ")
                print(cursor.fetchall())
                
                
            return connection
        
    except Error as e:
        return None

def execute_query(query, params=None):
    try:
        with create_connection() as connection:
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    resultados = cursor.fetchall()
                    return resultados
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None


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
