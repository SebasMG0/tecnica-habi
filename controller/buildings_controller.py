import os

import database.connector as connector

def get_buildings_query(filters:dict[str, list], status_filter_codes:dict[str, int]) -> str:
    """
        Generate a SQL query to retrieve building information based on the provided filters.

        Args:
            filters: A dictionary containing the filters to apply to the query.
            status_filter_codes: A dictionary mapping status codes to their names.
    """

    base_query = ("SELECT s.name, p.city, p.address, p.year, p.price, p.description "
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
                where_clauses.append(f"city IN ({', '.join( map(lambda city: f"'{str(city)}'", filters['city']) )})")
        
            else:
                raise ValueError("Invalid city filter")
        
        base_query += " WHERE " + " AND ".join(where_clauses)
    
    return base_query


def execute_query(status_filter_codes:dict[str, int], filters:dict[str, list], columns:list[str])-> dict:
    """
        Execute a query to the database and return the results.

        Args:
            status_filter_codes: A dictionary mapping status codes to their names.
            filters: A dictionary containing the filters to apply to the query.
            columns: A list of column names to include in the results.

        Returns:
            formatted_results: A list of dictionaries representing the query results, 
            where each dictionary corresponds to a row in the result set.
    """
    
    query= get_buildings_query(filters= filters, status_filter_codes= status_filter_codes)

    with connector.create_connection(host = os.getenv("HOST"), 
                                     port = os.getenv("PORT"),
                                     user = os.getenv("USER"),
                                     password = os.getenv("PASS"),
                                     database = os.getenv("SCHEMA")) as connection:
        if connection:
            results = connector.execute_query(connection= connection, query= query)
            formatted_results = [
                dict(zip(columns, row)) for row in results
            ]
            return formatted_results
        
        else:
            raise Exception("There was an error connecting to the database")
