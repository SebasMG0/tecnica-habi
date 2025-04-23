import os
from dotenv import load_dotenv
from database import connector
from api import api

if __name__ == "__main__":
    # Load variables from .env file
    load_dotenv(override=True)

    api.run()


    # with connector.create_connection(host= HOST, port=PORT, user=USER, password=PASS, database=SCHEMA) as connector:
        
    
    