def get_buildings_query(filters:dict, status_filter_codes:dict) -> str:
    base_query = ("SELECT sh.*, s.*, p.*"
                    "FROM status_history sh "
                    "INNER JOIN ( "
                        "SELECT property_id, MAX(update_date) AS last_update "
                        "FROM status_history "
                        "GROUP BY property_id) latest "
                    "ON sh.property_id = latest.property_id AND sh.update_date = latest.last_update "
                    "INNER JOIN status s ON sh.status_id = s.id "
                    "INNER JOIN property p ON sh.property_id = p.id) ")
                
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
                where_clauses.append(f"status = {filters['status'][0]}")

            else:
                where_clauses.append(f"status IN ({', '.join(map(str, filters['status']))})")
        
        if "city" in filters.keys():
            if len(filters["city"]) == 1:
                where_clauses.append(f"city = '{filters['city'][0]}'")

            elif len(filters["city"]) >= 2:
                where_clauses.append(f"city IN ({', '.join(map(str, filters['city']))})")
        
            else:
                raise ValueError("Invalid city filter")
        
        base_query += " WHERE " + " AND ".join(where_clauses)
    
    return base_query