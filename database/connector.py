import os
import mysql.connector
from mysql.connector import Error

def create_connection(host, port, user, password, database):
    """
        Create a database connection to the MySQL database server.
        
        Args:
            host: The hostname of the database server.
            port: The port number of the database server
            user: The username to connect to the database.
            password: The password to connect to the database.
            database: The name of the database to connect to.
            
        Returns:
            connection: A MySQLConnection object representing the connection to the database.
    """
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
        return {"code":500, "msg": "Internal server error"}


def execute_query(connection, query:str, params:list=None):
    """
        Execute a SQL query on the database.

        Args:
            connection: A MySQLConnection object representing the connection to the database.
            query: The SQL query to execute.
            params: Optional parameters for the SQL query.

        Returns:
            results: The results of the query as a list of tuples.
    """

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
