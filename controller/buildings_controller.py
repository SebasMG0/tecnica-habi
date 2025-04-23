import os
import database.connector as connector

def get_buildings_query(filters:dict, status_filter_codes:dict) -> str:
    base_query = ("SELECT sh.*, s.*, p.*"
                    "FROM status_history sh "
                    "INNER JOIN ( "
                        "SELECT property_id, MAX(update_date) AS last_update "
                        "FROM status_history "
                        "GROUP BY property_id) latest "
                    "ON sh.property_id = latest.property_id AND sh.update_date = latest.last_update "
                    "INNER JOIN status s ON sh.status_id = s.id "
                    "INNER JOIN property p ON sh.property_id = p.id ")
                
    where_clauses = []
    
    if filters:

        if "year" in filters.keys():
            if len(filters["year"]) == 1:
                where_clauses.append(f"year = {filters['year'][0]}")

            elif len(filters["year"]) == 2:
                where_clauses.append(f"year BETWEEN {filters['year'][0]} AND {filters['year'][1]}")

            elif len(filters["year"]) > 2:
                where_clauses.append(f"year IN ({', '.join(map(str, filters['year']))})")
        
            else:
                raise ValueError("Invalid year filter")

        if "status" in filters.keys():
            if (len(filters["status"]) > len(status_filter_codes)) or (not all([code in status_filter_codes.values() for code in filters["status"]])):          
                raise ValueError("Invalid status filter")
            
            elif len(filters["status"]) == 1:
                where_clauses.append(f"status_id = {filters['status'][0]}")

            else:
                where_clauses.append(f"status_id IN ({', '.join(map(str, filters['status']))})")
        
        if "city" in filters.keys():
            if len(filters["city"]) == 1:
                where_clauses.append(f"city = '{filters['city'][0]}'")

            elif len(filters["city"]) >= 2:
                where_clauses.append(f"city IN ({', '.join(map(lambda city: f"'{str(city)}'", filters['city']))})")
        
            else:
                raise ValueError("Invalid city filter")
        
        base_query += " WHERE " + " AND ".join(where_clauses)
        print(base_query)
    
    return base_query

def execute_query(status_filter_codes:dict, filters:dict):
    query= get_buildings_query(filters= filters, status_filter_codes= status_filter_codes)

    with connector.create_connection(host = os.getenv("HOST"), 
                                     port = os.getenv("PORT"),
                                     user = os.getenv("USER"),
                                     password = os.getenv("PASS"),
                                     database = os.getenv("SCHEMA")) as connection:
        if connection:
            return connector.execute_query(connection= connection, query= query)
        else:
            raise Exception("There was an error connecting to the database")