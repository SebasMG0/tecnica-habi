import os
from dotenv import load_dotenv
from database import connector
from api import api

if __name__ == "__main__":
    # Load variables from .env file
    load_dotenv(override=True)

    try:
        api.run()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        
    
    