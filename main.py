import os
from dotenv import load_dotenv
from database import connector
from api import api

if __name__ == "__main__":
    # Load variables from .env file
    load_dotenv(override=True)

    # Load environment variables
    HOST= os.getenv("HOST")
    PORT= os.getenv("PORT")
    USER= os.getenv("USER")
    PASS= os.getenv("PASS")
    SCHEMA= os.getenv("SCHEMA")


    with connector.create_connection(host= HOST, port=PORT, user=USER, password=PASS, database=SCHEMA) as connector:
        if connector:
            api.run()
        else:
            print("No se pudo establecer la conexión.")
    
    